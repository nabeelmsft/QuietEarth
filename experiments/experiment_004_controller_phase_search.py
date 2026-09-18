"""Experiment 004: autonomous search over Experiment 003 recordings."""

from src.controller import (
    ControllerConfig,
    MeasurementMode,
    RecordedMeasurementProvider,
    TonalController,
)
from src.controller.models import ControllerReport, ReacquisitionDecision


def run_experiment() -> tuple[ControllerReport, ReacquisitionDecision]:
    """Run the recorded-data controller demonstration and return its results."""
    provider = RecordedMeasurementProvider()
    baseline = provider.baseline_amplitude("left_speaker_only")
    config = ControllerConfig(
        target_frequency_hz=provider.metadata["target_frequency_hz"],
        candidate_phases_degrees=[345, 0, 15, 30, 45, 180],
        candidate_control_amplitude=1.0,
        measurement_duration_seconds=1.0,
        acoustic_settling_duration_seconds=0.25,
        measurements_per_phase=1,
        verification_trials=3,
        baseline_amplitude=baseline,
        minimum_required_reduction_percent=90.0,
        reacquisition_threshold=5.0,
        measurement_mode=MeasurementMode.RECORDED,
        numerical_floor=1e-12,
    )
    controller = TonalController(config, provider)
    report = controller.run()
    elevated_residual = config.reacquisition_threshold + 1.0
    return report, controller.assess_maintenance(elevated_residual)


def main() -> None:
    report, reacquisition = run_experiment()

    print("QUIETEARTH EXPERIMENT 004")
    print("Autonomous Tonal-Control State Search")
    print()
    print(f"Target frequency: {report.target_frequency_hz:g} Hz")
    print("Measurement source: Experiment 003 recorded physical acoustic data")
    print(f"Baseline amplitude: {report.baseline_amplitude:.6f}")
    print()
    print("PHASE EVALUATION")
    for evaluation in report.phase_evaluations:
        amplitudes = ", ".join(
            f"{value:.6f}"
            for value in evaluation.statistics.measured_amplitudes
        )
        print(
            f"{evaluation.display_phase_degrees:g} degrees: "
            f"[{amplitudes}] median={evaluation.statistics.median_amplitude:.6f}"
        )
    print()
    print(
        f"Selected control phase: {report.selected_display_phase_degrees:g} degrees"
    )
    verification = ", ".join(
        f"{value:.6f}" for value in report.verification.measured_amplitudes
    )
    print(f"Verification trials: [{verification}]")
    print(f"Verification mean: {report.verification.mean_amplitude:.6f}")
    print(f"Verification median: {report.verification.median_amplitude:.6f}")
    print(
        "Percentage amplitude reduction: "
        f"{report.reduction.percentage_amplitude_reduction:.6f}%"
    )
    print(
        "Amplitude-ratio reduction: "
        f"{report.reduction.amplitude_ratio_reduction_db:.6f} dB"
    )
    print(f"Controller state: {report.controller_state}")
    print(
        "Reacquisition required: "
        f"{str(reacquisition.reacquisition_required).upper()}"
    )
    print(f"Reacquisition state: {reacquisition.resulting_state}")
    print()
    print("MEASUREMENT_SOURCE: PHYSICAL_RECORDINGS")
    print("PHYSICAL_ACOUSTIC_ACQUISITION: TRUE")
    print("AUTONOMOUS_LIVE_CONTROL: FALSE")
    print("ACTIVE_ACOUSTIC_APERTURE_VALIDATED: FALSE")
    print("DATACENTER_FIELD_VALIDATED: FALSE")


if __name__ == "__main__":
    main()
