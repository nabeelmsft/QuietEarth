"""Experiment 002: propagation delay and phase compensation."""

from src.acoustic_model import (
    PropagatedCancellationResult,
    simulate_propagated_tonal_cancellation,
)

FREQUENCY_HZ = 120.0
SAMPLE_RATE_HZ = 8000
SPEED_OF_SOUND_M_S = 343.0
PRIMARY_DISTANCE_M = 1.0
MISMATCHED_CONTROL_DISTANCE_M = (
    PRIMARY_DISTANCE_M + SPEED_OF_SOUND_M_S / (4 * FREQUENCY_HZ)
)


def _format_reduction(result: PropagatedCancellationResult) -> str:
    reduction_db = result.metrics.reduction_db
    return (
        "IDEAL NUMERICAL CANCELLATION (BELOW FLOATING-POINT FLOOR)"
        if reduction_db is None
        else f"{reduction_db:.6f} dB"
    )


def _print_scenario(
    label: str,
    description: str,
    result: PropagatedCancellationResult,
) -> None:
    primary_delay_ms = result.primary_path.delay_seconds * 1000
    control_delay_ms = result.control_path.delay_seconds * 1000
    delay_difference_ms = control_delay_ms - primary_delay_ms

    print(label)
    print(description)
    print(f"Primary path: {result.primary_path.distance_m:.6f} m")
    print(f"Control path: {result.control_path.distance_m:.6f} m")
    print(f"Primary propagation delay: {primary_delay_ms:.6f} ms")
    print(f"Control propagation delay: {control_delay_ms:.6f} ms")
    print(f"Propagation delay difference: {delay_difference_ms:.6f} ms")
    print(
        "Effective phase difference: "
        f"{result.effective_phase_difference_degrees:.6f} degrees"
    )
    print(
        "Compensation: "
        f"{'ON' if result.compensation_enabled else 'OFF'}"
    )
    if result.compensation_enabled:
        compensation = result.control_phase_offset_degrees - 180.0
        print(f"Calculated compensation: {compensation:.6f} degrees")
    print(f"RMS before control: {result.metrics.rms_before:.12g}")
    print(f"RMS after control: {result.metrics.rms_after:.12g}")
    print(f"Residual energy: {result.metrics.energy_after:.12g}")
    print(
        "Residual energy ratio: "
        f"{result.metrics.residual_energy_ratio:.12g}"
    )
    print(f"Reduction: {_format_reduction(result)}")
    print()


def main() -> None:
    scenario_a = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=PRIMARY_DISTANCE_M,
        compensation_enabled=False,
        sample_rate_hz=SAMPLE_RATE_HZ,
        speed_of_sound_m_s=SPEED_OF_SOUND_M_S,
    )
    scenario_b = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=MISMATCHED_CONTROL_DISTANCE_M,
        compensation_enabled=False,
        sample_rate_hz=SAMPLE_RATE_HZ,
        speed_of_sound_m_s=SPEED_OF_SOUND_M_S,
    )
    scenario_c = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=MISMATCHED_CONTROL_DISTANCE_M,
        compensation_enabled=True,
        sample_rate_hz=SAMPLE_RATE_HZ,
        speed_of_sound_m_s=SPEED_OF_SOUND_M_S,
    )

    print("QUIETEARTH EXPERIMENT 002")
    print("Propagation Delay and Phase Compensation")
    print()
    print(f"Frequency: {FREQUENCY_HZ:g} Hz")
    print(f"Speed of sound: {SPEED_OF_SOUND_M_S:g} m/s")
    print()
    _print_scenario(
        "SCENARIO A",
        "Equal propagation paths",
        scenario_a,
    )
    _print_scenario(
        "SCENARIO B",
        "Mismatched propagation paths",
        scenario_b,
    )
    _print_scenario(
        "SCENARIO C",
        "Same mismatched geometry with propagation compensation",
        scenario_c,
    )
    print("SIMULATION: TRUE")
    print("PHYSICAL VALIDATION: FALSE")
    print("FIELD VALIDATED: FALSE")


if __name__ == "__main__":
    main()
