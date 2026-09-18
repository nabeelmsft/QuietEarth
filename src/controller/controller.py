"""Provider-independent tonal phase search and maintenance decisions."""

from __future__ import annotations

import math

from .models import (
    ControllerConfig,
    ControllerReport,
    ControllerState,
    MeasurementRequest,
    MeasurementResult,
    MeasurementStatistics,
    PhaseEvaluation,
    ReacquisitionDecision,
    ReductionMetrics,
    ReinforcingConditionImprovement,
    calculate_measurement_statistics,
    normalize_phase,
    normalized_absolute_phase,
)
from .providers import MeasurementProvider


def calculate_reduction_metrics(
    baseline_amplitude: float,
    residual_amplitude: float,
    numerical_floor: float,
) -> ReductionMetrics:
    """Calculate finite amplitude-ratio reduction metrics."""
    values = (baseline_amplitude, residual_amplitude, numerical_floor)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("reduction metric inputs must be finite")
    if baseline_amplitude <= 0:
        raise ValueError("baseline amplitude must be positive")
    if residual_amplitude < 0:
        raise ValueError("residual amplitude must be non-negative")
    if numerical_floor <= 0:
        raise ValueError("numerical floor must be positive")

    effective_residual = max(residual_amplitude, numerical_floor)
    ratio = effective_residual / baseline_amplitude
    return ReductionMetrics(
        baseline_amplitude=baseline_amplitude,
        selected_residual_amplitude=residual_amplitude,
        effective_residual_amplitude=effective_residual,
        absolute_amplitude_reduction=baseline_amplitude - residual_amplitude,
        residual_amplitude_ratio=ratio,
        percentage_amplitude_reduction=(1.0 - ratio) * 100.0,
        amplitude_ratio_reduction_db=20.0
        * math.log10(baseline_amplitude / effective_residual),
    )


class TonalController:
    """Search measured phases, verify the winner, and model maintenance."""

    def __init__(
        self, config: ControllerConfig, provider: MeasurementProvider
    ) -> None:
        self.config = config
        self.provider = provider

    def _request_measurements(
        self, phase_degrees: float, count: int, purpose: str
    ) -> list[MeasurementResult]:
        results = []
        for trial_number in range(1, count + 1):
            request = MeasurementRequest(
                target_frequency_hz=self.config.target_frequency_hz,
                phase_degrees=phase_degrees,
                control_amplitude=self.config.candidate_control_amplitude,
                trial_identifier=f"{purpose}-{trial_number}",
                measurement_duration_seconds=self.config.measurement_duration_seconds,
                acoustic_settling_duration_seconds=(
                    self.config.acoustic_settling_duration_seconds
                ),
            )
            result = self.provider.measure(request)
            if not math.isclose(
                normalize_phase(result.request.phase_degrees),
                normalize_phase(phase_degrees),
                abs_tol=1e-9,
            ):
                raise ValueError("measurement provider returned the wrong phase")
            results.append(result)
        return results

    def _evaluate_phase(self, display_phase: float) -> PhaseEvaluation:
        results = self._request_measurements(
            display_phase, self.config.measurements_per_phase, "search"
        )
        first = results[0]
        expected_physical = self.config.measurement_mode.value in {"recorded", "live"}
        expected_simulated = self.config.measurement_mode.value == "simulated"
        if (
            first.is_physical_recording != expected_physical
            or first.is_simulated != expected_simulated
        ):
            raise ValueError(
                "measurement provenance does not match configured measurement mode"
            )
        if any(
            result.measurement_source != first.measurement_source
            or result.is_physical_recording != first.is_physical_recording
            or result.is_simulated != first.is_simulated
            for result in results[1:]
        ):
            raise ValueError("measurements for one phase must share provenance")
        return PhaseEvaluation(
            display_phase_degrees=display_phase,
            normalized_phase_degrees=normalize_phase(display_phase),
            statistics=calculate_measurement_statistics(
                [result.measured_amplitude for result in results]
            ),
            measurement_source=first.measurement_source,
            is_physical_recording=first.is_physical_recording,
            is_simulated=first.is_simulated,
            available_verification_measurements=(
                self.provider.available_measurement_count(
                    self.config.target_frequency_hz, display_phase
                )
            ),
        )

    def select_best_phase(
        self, evaluations: list[PhaseEvaluation]
    ) -> PhaseEvaluation:
        """Select the lowest median with deterministic tolerance tie-breaking."""
        if not evaluations:
            raise ValueError("at least one phase evaluation is required")
        lowest_median = min(
            evaluation.statistics.median_amplitude for evaluation in evaluations
        )
        tied = [
            evaluation
            for evaluation in evaluations
            if evaluation.statistics.median_amplitude
            <= lowest_median + self.config.selection_tolerance
        ]
        return min(
            tied,
            key=lambda evaluation: (
                evaluation.statistics.standard_deviation,
                -evaluation.available_verification_measurements,
                normalized_absolute_phase(evaluation.normalized_phase_degrees),
                evaluation.normalized_phase_degrees,
            ),
        )

    def _reinforcing_improvement(
        self,
        evaluations: list[PhaseEvaluation],
        selected_residual: float,
    ) -> ReinforcingConditionImprovement | None:
        reinforcing = next(
            (
                evaluation
                for evaluation in evaluations
                if math.isclose(
                    evaluation.normalized_phase_degrees, 180.0, abs_tol=1e-9
                )
            ),
            None,
        )
        if reinforcing is None:
            return None
        metrics = calculate_reduction_metrics(
            reinforcing.statistics.median_amplitude,
            selected_residual,
            self.config.numerical_floor,
        )
        return ReinforcingConditionImprovement(
            reinforcing_phase_degrees=reinforcing.display_phase_degrees,
            reinforcing_amplitude=reinforcing.statistics.median_amplitude,
            absolute_amplitude_reduction=metrics.absolute_amplitude_reduction,
            percentage_amplitude_reduction=metrics.percentage_amplitude_reduction,
            amplitude_ratio_reduction_db=metrics.amplitude_ratio_reduction_db,
        )

    def run(self) -> ControllerReport:
        """Run one deterministic SEARCH, VERIFY, and state-transition cycle."""
        evaluations = [
            self._evaluate_phase(phase)
            for phase in self.config.candidate_phases_degrees
        ]
        selected = self.select_best_phase(evaluations)
        verification_results = self._request_measurements(
            selected.display_phase_degrees,
            self.config.verification_trials,
            "verification",
        )
        verification = calculate_measurement_statistics(
            [result.measured_amplitude for result in verification_results]
        )
        reduction = calculate_reduction_metrics(
            self.config.baseline_amplitude,
            verification.median_amplitude,
            self.config.numerical_floor,
        )
        state = (
            ControllerState.MAINTAIN
            if reduction.percentage_amplitude_reduction
            >= self.config.minimum_required_reduction_percent
            else ControllerState.VERIFICATION_FAILED
        )
        return ControllerReport(
            target_frequency_hz=self.config.target_frequency_hz,
            measurement_mode=self.config.measurement_mode,
            baseline_amplitude=self.config.baseline_amplitude,
            phase_evaluations=evaluations,
            selected_display_phase_degrees=selected.display_phase_degrees,
            selected_normalized_phase_degrees=selected.normalized_phase_degrees,
            verification=verification,
            reduction=reduction,
            reinforcing_condition_improvement=self._reinforcing_improvement(
                evaluations, verification.median_amplitude
            ),
            controller_state=state,
            minimum_required_reduction_percent=(
                self.config.minimum_required_reduction_percent
            ),
            scientific_validation_labels={
                "measurement_source": (
                    "PHYSICAL_RECORDINGS"
                    if self.config.measurement_mode.value == "recorded"
                    else (
                        "LIVE_MICROPHONE"
                        if self.config.measurement_mode.value == "live"
                        else "SIMULATION"
                    )
                ),
                "physical_acoustic_acquisition": selected.is_physical_recording,
                "autonomous_live_control": False,
                "active_acoustic_aperture_validated": False,
                "datacenter_field_validated": False,
            },
        )

    def assess_maintenance(self, measured_amplitude: float) -> ReacquisitionDecision:
        """Decide whether a later residual requires phase reacquisition."""
        if not math.isfinite(measured_amplitude) or measured_amplitude < 0:
            raise ValueError("maintenance amplitude must be finite and non-negative")
        required = measured_amplitude > self.config.reacquisition_threshold
        return ReacquisitionDecision(
            measured_amplitude=measured_amplitude,
            threshold=self.config.reacquisition_threshold,
            reacquisition_required=required,
            resulting_state=(
                ControllerState.REACQUIRE if required else ControllerState.MAINTAIN
            ),
        )
