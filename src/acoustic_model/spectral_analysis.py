"""Frequency-domain analysis for simulated acoustic signals."""

import numpy as np
from numpy.typing import ArrayLike, NDArray


def compute_fft(
    signal: ArrayLike, sample_rate_hz: int
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return one-sided FFT frequencies and amplitudes."""
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


def find_dominant_frequencies(
    signal: ArrayLike, sample_rate_hz: int, top_n: int = 5
) -> list[float]:
    """Return the strongest non-DC frequency peaks by descending amplitude."""
    if isinstance(top_n, bool) or not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer")

    frequencies, amplitudes = compute_fft(signal, sample_rate_hz)
    if frequencies.size < 2:
        return []

    non_dc_amplitudes = amplitudes[1:]
    is_peak = np.ones(non_dc_amplitudes.size, dtype=np.bool_)
    if non_dc_amplitudes.size > 1:
        is_peak[1:] &= non_dc_amplitudes[1:] > non_dc_amplitudes[:-1]
        is_peak[:-1] &= non_dc_amplitudes[:-1] >= non_dc_amplitudes[1:]

    peak_indices = np.flatnonzero(is_peak) + 1
    strongest = peak_indices[
        np.argsort(amplitudes[peak_indices])[-top_n:][::-1]
    ]
    return frequencies[strongest].tolist()
