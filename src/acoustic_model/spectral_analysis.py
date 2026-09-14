"""Frequency-domain analysis for simulated acoustic signals."""

import numpy as np
from numpy.typing import ArrayLike, NDArray


def compute_spectrum(
    signal: ArrayLike, sample_rate_hz: int
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return one-sided frequencies and amplitude spectrum."""
    samples = np.asarray(signal, dtype=np.float64)
    if samples.ndim != 1 or samples.size == 0:
        raise ValueError("signal must be a non-empty one-dimensional sequence")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")

    frequencies = np.fft.rfftfreq(samples.size, d=1 / sample_rate_hz)
    amplitudes = 2 * np.abs(np.fft.rfft(samples)) / samples.size
    amplitudes[0] /= 2
    if samples.size % 2 == 0:
        amplitudes[-1] /= 2

    return frequencies, amplitudes


def dominant_frequencies(
    signal: ArrayLike, sample_rate_hz: int, count: int = 3
) -> list[float]:
    """Return the strongest non-DC frequencies in descending amplitude order."""
    if count < 1:
        raise ValueError("count must be at least 1")

    frequencies, amplitudes = compute_spectrum(signal, sample_rate_hz)
    available_count = min(count, max(0, frequencies.size - 1))
    strongest = np.argsort(amplitudes[1:])[-available_count:][::-1] + 1
    return frequencies[strongest].tolist()
