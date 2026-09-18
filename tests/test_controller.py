import math

import pytest
from pydantic import ValidationError

from src.controller import (
    ControllerConfig,
    ControllerState,
    MeasurementMode,
    MeasurementRequest,
    MeasurementResult,
    RecordedMeasurementProvider,
    SimulationMeasurementProvider,
    TonalController,
    calculate_measurement_statistics,
    calculate_reduction_metrics,
    normalize_phase,
)


def _config(**overrides: object) -> ControllerConfig:
    values: dict[str, object] = {
        "target_frequency_hz": 200,
        "candidate_phases_degrees": [0, 45, 180],
        "candidate_control_amplitude": 1.0,
        "measurement_duration_seconds": 1.0,
        "acoustic_settling_duration_seconds": 0.25,
        "measurements_per_phase": 1,
        "verification_trials": 1,
        "baseline_amplitude": 10.0,
        "minimum_required_reduction_percent": 50.0,
        "reacquisition_threshold": 4.0,
        "measurement_mode": MeasurementMode.SIMULATED,
        "numerical_floor": 1e-12,
    }
    values.update(overrides)
    return ControllerConfig(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("candidate_phases_degrees", []),
        ("target_frequency_hz", 0),
        ("target_frequency_hz", -1),
        ("measurements_per_phase", 0),
        ("verification_trials", 0),
        ("measurement_duration_seconds", 0),
        ("acoustic_settling_duration_seconds", -0.1),
        ("numerical_floor", 0),
    ],
)
def test_invalid_controller_configuration_is_rejected(
    field: str, value: object
) -> None:
    with pytest.raises(ValidationError):
        _config(**{field: value})


def test_missing_baseline_is_rejected() -> None:
    values = _config().model_dump()
    del values["baseline_amplitude"]

    with pytest.raises(ValidationError):
        ControllerConfig(**values)


@pytest.mark.parametrize(
    ("phase", "expected"),
    [(-15, 345), (360, 0), (735, 15), (45, 45)],
)
def test_phase_normalization(phase: float, expected: float) -> None:
    assert normalize_phase(phase) == pytest.approx(expected)


def test_duplicate_normalized_phases_are_rejected() -> None:
    with pytest.raises(ValidationError, match="unique after normalization"):
        _config(candidate_phases_degrees=[0, 360])


def test_measurement_statistics_include_mean_median_and_population_deviation() -> None:
    statistics = calculate_measurement_statistics([1.0, 2.0, 6.0])

    assert statistics.mean_amplitude == pytest.approx(3.0)
    assert statistics.median_amplitude == pytest.approx(2.0)
    assert statistics.minimum_amplitude == 1.0
    assert statistics.maximum_amplitude == 6.0
    assert statistics.standard_deviation == pytest.approx(math.sqrt(14 / 3))
    assert statistics.measurement_count == 3


def test_negative_measurement_amplitude_is_rejected() -> None:
    request = MeasurementRequest(
        target_frequency_hz=200,
        phase_degrees=0,
        control_amplitude=1,
        trial_identifier="test-1",
        measurement_duration_seconds=1,
        acoustic_settling_duration_seconds=0,
    )

    with pytest.raises(ValidationError):
        MeasurementResult(
            request=request,
            measured_amplitude=-1,
            measurement_source="invalid",
            is_physical_recording=False,
            is_simulated=True,
        )


def test_controller_selects_lowest_median_not_a_hard_coded_phase() -> None:
    landscape = {0.0: 4.0, 45.0: 3.0, 120.0: 0.5, 180.0: 12.0}
    provider = SimulationMeasurementProvider(
        lambda request: landscape[normalize_phase(request.phase_degrees)]
    )
    controller = TonalController(
        _config(candidate_phases_degrees=[0, 45, 120, 180]), provider
    )

    report = controller.run()

    assert report.selected_normalized_phase_degrees == 120
    assert report.controller_state == ControllerState.MAINTAIN
    assert all(evaluation.is_simulated for evaluation in report.phase_evaluations)
    assert not any(
        evaluation.is_physical_recording
        for evaluation in report.phase_evaluations
    )


def test_tie_breaking_prefers_lower_variation() -> None:
    values = {
        (10.0, 1): 0.0,
        (10.0, 2): 2.0,
        (20.0, 1): 1.0,
        (20.0, 2): 1.0,
    }

    def response(request: MeasurementRequest) -> float:
        trial = int(request.trial_identifier.rsplit("-", 1)[1])
        return values[(normalize_phase(request.phase_degrees), trial)]

    controller = TonalController(
        _config(
            candidate_phases_degrees=[10, 20],
            measurements_per_phase=2,
            verification_trials=2,
        ),
        SimulationMeasurementProvider(response),
    )

    assert controller.run().selected_normalized_phase_degrees == 20


def test_tie_breaking_prefers_more_available_trials_then_lower_absolute_phase() -> None:
    class CountedSimulationProvider(SimulationMeasurementProvider):
        def available_measurement_count(
            self, target_frequency_hz: float, phase_degrees: float
        ) -> int:
            del target_frequency_hz
            return 3 if normalize_phase(phase_degrees) == 20 else 1

    more_trials = TonalController(
        _config(candidate_phases_degrees=[10, 20]),
        CountedSimulationProvider(lambda request: 1.0),
    )
    equal_trials = TonalController(
        _config(candidate_phases_degrees=[350, 20]),
        SimulationMeasurementProvider(lambda request: 1.0),
    )

    assert more_trials.run().selected_normalized_phase_degrees == 20
    assert equal_trials.run().selected_normalized_phase_degrees == 350


def test_reduction_metrics_use_amplitude_ratio_formula() -> None:
    metrics = calculate_reduction_metrics(10, 1, 1e-12)

    assert metrics.absolute_amplitude_reduction == pytest.approx(9)
    assert metrics.residual_amplitude_ratio == pytest.approx(0.1)
    assert metrics.percentage_amplitude_reduction == pytest.approx(90)
    assert metrics.amplitude_ratio_reduction_db == pytest.approx(20)


def test_numerical_floor_prevents_infinite_reduction() -> None:
    metrics = calculate_reduction_metrics(1, 0, 1e-9)

    assert metrics.selected_residual_amplitude == 0
    assert metrics.effective_residual_amplitude == pytest.approx(1e-9)
    assert metrics.amplitude_ratio_reduction_db == pytest.approx(180)
    assert math.isfinite(metrics.amplitude_ratio_reduction_db)


def test_verification_aggregation_and_maintain_state() -> None:
    trial_values = [1.0, 2.0, 3.0]

    def response(request: MeasurementRequest) -> float:
        if request.trial_identifier.startswith("verification"):
            trial = int(request.trial_identifier.rsplit("-", 1)[1])
            return trial_values[trial - 1]
        return 1.5

    report = TonalController(
        _config(
            candidate_phases_degrees=[90],
            verification_trials=3,
            baseline_amplitude=10,
            minimum_required_reduction_percent=75,
        ),
        SimulationMeasurementProvider(response),
    ).run()

    assert report.verification.measured_amplitudes == trial_values
    assert report.verification.mean_amplitude == pytest.approx(2)
    assert report.verification.median_amplitude == pytest.approx(2)
    assert report.controller_state == ControllerState.MAINTAIN


def test_failed_minimum_reduction_does_not_enter_maintain() -> None:
    report = TonalController(
        _config(candidate_phases_degrees=[0], minimum_required_reduction_percent=90),
        SimulationMeasurementProvider(lambda request: 5.0),
    ).run()

    assert report.controller_state == ControllerState.VERIFICATION_FAILED


def test_reacquisition_threshold_behavior() -> None:
    controller = TonalController(
        _config(candidate_phases_degrees=[0]),
        SimulationMeasurementProvider(lambda request: 1.0),
    )

    at_threshold = controller.assess_maintenance(4.0)
    above_threshold = controller.assess_maintenance(4.01)

    assert not at_threshold.reacquisition_required
    assert at_threshold.resulting_state == ControllerState.MAINTAIN
    assert above_threshold.reacquisition_required
    assert above_threshold.resulting_state == ControllerState.REACQUIRE


def _recorded_controller() -> TonalController:
    provider = RecordedMeasurementProvider()
    return TonalController(
        _config(
            target_frequency_hz=200,
            candidate_phases_degrees=[345, 0, 15, 30, 45, 180],
            measurements_per_phase=1,
            verification_trials=3,
            baseline_amplitude=provider.baseline_amplitude("left_speaker_only"),
            minimum_required_reduction_percent=90,
            measurement_mode=MeasurementMode.RECORDED,
        ),
        provider,
    )


def test_experiment_003_selects_45_and_preserves_physical_trials() -> None:
    report = _recorded_controller().run()

    assert report.selected_normalized_phase_degrees == 45
    assert report.verification.measured_amplitudes == [
        1.284177,
        0.844939,
        0.565633,
    ]
    assert report.verification.mean_amplitude == pytest.approx(0.8982496667)
    assert report.controller_state == ControllerState.MAINTAIN
    assert all(
        evaluation.is_physical_recording
        for evaluation in report.phase_evaluations
    )
    assert not any(evaluation.is_simulated for evaluation in report.phase_evaluations)


def test_experiment_003_rejects_180_as_attenuation() -> None:
    report = _recorded_controller().run()
    reinforcing = next(
        evaluation
        for evaluation in report.phase_evaluations
        if evaluation.normalized_phase_degrees == 180
    )

    assert reinforcing.statistics.median_amplitude > report.baseline_amplitude
    assert report.selected_normalized_phase_degrees != 180
    assert report.reinforcing_condition_improvement is not None
    assert (
        report.reinforcing_condition_improvement.reinforcing_amplitude
        == reinforcing.statistics.median_amplitude
    )


def test_recorded_provider_does_not_interpolate_missing_phases() -> None:
    provider = RecordedMeasurementProvider()
    request = MeasurementRequest(
        target_frequency_hz=200,
        phase_degrees=60,
        control_amplitude=1,
        trial_identifier="search-1",
        measurement_duration_seconds=1,
        acoustic_settling_duration_seconds=0,
    )

    with pytest.raises(LookupError, match="no recorded physical measurement"):
        provider.measure(request)
