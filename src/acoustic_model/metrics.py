"""Metrics for comparing simulated acoustic signals."""

import numpy as np
from numpy.typing import ArrayLike


def tonal_reduction_db(reference: ArrayLike, residual: ArrayLike) -> float:
    """Calculate RMS reduction from a reference signal to a residual signal."""
    reference_samples = np.asarray(reference, dtype=np.float64)
    residual_samples = np.asarray(residual, dtype=np.float64)

    if reference_samples.shape != residual_samples.shape or reference_samples.size == 0:
        raise ValueError("reference and residual must be non-empty and have equal shapes")

    reference_rms = float(np.sqrt(np.mean(np.square(reference_samples))))
    residual_rms = float(np.sqrt(np.mean(np.square(residual_samples))))
    if reference_rms == 0:
        raise ValueError("reference signal must contain energy")
    if residual_rms == 0:
        return float("inf")

    return 20 * np.log10(reference_rms / residual_rms)
