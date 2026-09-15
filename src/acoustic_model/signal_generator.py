"""Deterministic synthetic tonal-signal generation."""

import numpy as np
from numpy.typing import NDArray


def generate_tone(
    frequency_hz: float,
    duration_seconds: float,
    sample_rate_hz: int = 8000,
    amplitude: float = 1.0,
    phase_degrees: float = 0.0,
) -> NDArray[np.float64]:
    """Generate a sine wave as a one-dimensional NumPy array."""
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    if frequency_hz >= sample_rate_hz / 2:
        raise ValueError("frequency_hz must be below the Nyquist frequency")
    if not np.isfinite(amplitude):
        raise ValueError("amplitude must be finite")
    if not np.isfinite(phase_degrees):
        raise ValueError("phase_degrees must be finite")

    sample_count = round(duration_seconds * sample_rate_hz)
    if sample_count < 1:
        raise ValueError("duration_seconds is too short for the sample rate")

    time = np.arange(sample_count, dtype=np.float64) / sample_rate_hz
    phase_radians = np.deg2rad(phase_degrees)
    return amplitude * np.sin(2 * np.pi * frequency_hz * time + phase_radians)


def generate_harmonic_signal(
    fundamental_hz: float,
    harmonics: int = 3,
    duration_seconds: float = 5,
    sample_rate_hz: int = 8000,
) -> NDArray[np.float64]:
    """Generate a fundamental tone and successively quieter harmonics."""
    if fundamental_hz <= 0:
        raise ValueError("fundamental_hz must be positive")
    if isinstance(harmonics, bool) or not isinstance(harmonics, int) or harmonics < 1:
        raise ValueError("harmonics must be a positive integer")
    signal = generate_tone(
        frequency_hz=fundamental_hz,
        duration_seconds=duration_seconds,
        sample_rate_hz=sample_rate_hz,
    )
    if fundamental_hz * harmonics >= sample_rate_hz / 2:
        raise ValueError("all generated tones must be below the Nyquist frequency")

    for harmonic in range(2, harmonics + 1):
        signal += generate_tone(
            frequency_hz=fundamental_hz * harmonic,
            duration_seconds=duration_seconds,
            sample_rate_hz=sample_rate_hz,
            amplitude=1 / harmonic,
        )

    return signal
