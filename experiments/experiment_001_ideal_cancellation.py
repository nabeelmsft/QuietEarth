"""Experiment 001: idealized pure-tone waveform cancellation."""

from src.acoustic_model import simulate_ideal_tonal_cancellation


def main() -> None:
    frequency_hz = 120.0
    result = simulate_ideal_tonal_cancellation(frequency_hz=frequency_hz)
    metrics = result.metrics
    reduction = (
        "IDEAL NUMERICAL CANCELLATION (BELOW FLOATING-POINT FLOOR)"
        if metrics.reduction_db is None
        else f"{metrics.reduction_db:.6f} dB"
    )

    print("QUIETEARTH EXPERIMENT 001")
    print("Ideal Tonal Cancellation Simulation")
    print()
    print(f"Primary frequency: {frequency_hz:g} Hz")
    print(f"Control frequency: {frequency_hz:g} Hz")
    print("Control phase offset: 180 degrees")
    print()
    print("Control OFF:")
    print(f"RMS: {metrics.rms_before:.12g}")
    print(f"Energy: {metrics.energy_before:.12g}")
    print()
    print("Control ON:")
    print(f"RMS: {metrics.rms_after:.12g}")
    print(f"Energy: {metrics.energy_after:.12g}")
    print()
    print(f"Reduction: {reduction}")
    print(f"Residual energy ratio: {metrics.residual_energy_ratio:.12g}")
    print()
    print("SIMULATION: TRUE")
    print("PHYSICAL VALIDATION: FALSE")
    print("FIELD VALIDATED: FALSE")


if __name__ == "__main__":
    main()
