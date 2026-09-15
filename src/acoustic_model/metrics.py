"""Metrics for comparing simulated acoustic signals."""

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _validated_signal(signal: ArrayLike) -> NDArray[np.float64]:
    samples = np.asarray(signal, dtype=np.float64)
    if samples.ndim != 1 or samples.size == 0:
        raise ValueError("signal must be a non-empty one-dimensional sequence")
    if not np.isfinite(samples).all():
        raise ValueError("signal must contain only finite values")
    return samples


def calculate_peak_level(signal: ArrayLike) -> float:
    """Return the largest absolute sample value."""
    samples = _validated_signal(signal)
    return float(np.max(np.abs(samples)))


def calculate_rms(signal: ArrayLike) -> float:
    """Return the root mean square of the signal."""
    samples = _validated_signal(signal)
    return float(np.sqrt(np.mean(np.square(samples))))


def calculate_signal_energy(signal: ArrayLike) -> float:
    """Return the sum of squared sample values."""
    samples = _validated_signal(signal)
    return float(np.sum(np.square(samples)))


def tonal_reduction_db(reference: ArrayLike, residual: ArrayLike) -> float:
    """Calculate RMS reduction from a reference signal to a residual signal."""
    reference_samples = _validated_signal(reference)
    residual_samples = _validated_signal(residual)

    if reference_samples.shape != residual_samples.shape:
        raise ValueError("reference and residual must have equal shapes")

    reference_rms = calculate_rms(reference_samples)
    residual_rms = calculate_rms(residual_samples)
    if reference_rms == 0:
        raise ValueError("reference signal must contain energy")
    if residual_rms == 0:
        return float("inf")

    return 20 * np.log10(reference_rms / residual_rms)
