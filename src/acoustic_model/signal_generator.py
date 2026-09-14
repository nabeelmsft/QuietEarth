"""Deterministic synthetic tonal-signal generation."""

import numpy as np
from numpy.typing import NDArray


def generate_tonal_signal(
    fundamental_hz: float,
    harmonic_count: int,
    duration_seconds: float,
    sample_rate_hz: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Generate a fundamental tone and successively quieter harmonics."""
    if fundamental_hz <= 0:
        raise ValueError("fundamental_hz must be positive")
    if harmonic_count < 1:
        raise ValueError("harmonic_count must be at least 1")
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    if fundamental_hz * harmonic_count >= sample_rate_hz / 2:
        raise ValueError("all generated tones must be below the Nyquist frequency")

    sample_count = round(duration_seconds * sample_rate_hz)
    if sample_count < 1:
        raise ValueError("duration_seconds is too short for the sample rate")

    time = np.arange(sample_count, dtype=np.float64) / sample_rate_hz
    signal = np.zeros(sample_count, dtype=np.float64)

    for harmonic in range(1, harmonic_count + 1):
        signal += np.sin(2 * np.pi * fundamental_hz * harmonic * time) / harmonic

    return time, signal
