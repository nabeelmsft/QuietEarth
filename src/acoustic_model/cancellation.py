"""Idealized waveform-superposition cancellation simulation."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .metrics import (
    calculate_peak_level,
    calculate_rms,
    calculate_signal_energy,
    tonal_reduction_db,
)
from .signal_generator import generate_tone


@dataclass(frozen=True)
class CancellationMetrics:
    """Before-and-after measurements for simulated cancellation."""

    rms_before: float
    rms_after: float
    energy_before: float
    energy_after: float
    residual_energy_ratio: float
    reduction_db: float | None


@dataclass(frozen=True)
class CancellationResult:
    """Signals and metrics produced by an ideal cancellation simulation."""

    primary_signal: NDArray[np.float64]
    control_signal: NDArray[np.float64]
    residual_signal: NDArray[np.float64]
    metrics: CancellationMetrics


def generate_control_signal(
    frequency_hz: float,
    amplitude: float,
    phase_offset_degrees: float,
    duration_seconds: float,
    sample_rate_hz: int = 8000,
) -> NDArray[np.float64]:
    """Generate an ideal control tone with an explicit phase offset."""
    return generate_tone(
        frequency_hz=frequency_hz,
        duration_seconds=duration_seconds,
        sample_rate_hz=sample_rate_hz,
        amplitude=amplitude,
        phase_degrees=phase_offset_degrees,
    )


def combine_signals(
    primary_signal: ArrayLike, control_signal: ArrayLike
) -> NDArray[np.float64]:
    """Superimpose equal-length primary and control signals."""
    primary = np.asarray(primary_signal, dtype=np.float64)
    control = np.asarray(control_signal, dtype=np.float64)
    if primary.ndim != 1 or control.ndim != 1 or primary.size == 0:
        raise ValueError("signals must be non-empty one-dimensional sequences")
    if primary.shape != control.shape:
        raise ValueError("primary and control signals must have equal shapes")
    if not np.isfinite(primary).all() or not np.isfinite(control).all():
        raise ValueError("signals must contain only finite values")
    return primary + control


def calculate_cancellation_metrics(
    primary_signal: ArrayLike, residual_signal: ArrayLike
) -> CancellationMetrics:
    """Calculate cancellation metrics without reporting infinite reduction."""
    primary = np.asarray(primary_signal, dtype=np.float64)
    residual = np.asarray(residual_signal, dtype=np.float64)
    if primary.shape != residual.shape:
        raise ValueError("primary and residual signals must have equal shapes")

    rms_before = calculate_rms(primary)
    rms_after = calculate_rms(residual)
    energy_before = calculate_signal_energy(primary)
    energy_after = calculate_signal_energy(residual)
    if energy_before == 0:
        raise ValueError("primary signal must contain energy")

    numerical_floor = (
        1000
        * np.finfo(np.float64).eps
        * max(1.0, calculate_peak_level(primary))
    )
    reduction_db = (
        None
        if rms_after <= numerical_floor
        else tonal_reduction_db(primary, residual)
    )

    return CancellationMetrics(
        rms_before=rms_before,
        rms_after=rms_after,
        energy_before=energy_before,
        energy_after=energy_after,
        residual_energy_ratio=energy_after / energy_before,
        reduction_db=reduction_db,
    )


def simulate_ideal_tonal_cancellation(
    frequency_hz: float = 120.0,
    amplitude: float = 1.0,
    duration_seconds: float = 5.0,
    sample_rate_hz: int = 8000,
) -> CancellationResult:
    """Simulate equal-amplitude, 180-degree cancellation of a pure tone."""
    primary = generate_tone(
        frequency_hz=frequency_hz,
        duration_seconds=duration_seconds,
        sample_rate_hz=sample_rate_hz,
        amplitude=amplitude,
    )
    control = generate_control_signal(
        frequency_hz=frequency_hz,
        amplitude=amplitude,
        phase_offset_degrees=180.0,
        duration_seconds=duration_seconds,
        sample_rate_hz=sample_rate_hz,
    )
    residual = combine_signals(primary, control)
    return CancellationResult(
        primary_signal=primary,
        control_signal=control,
        residual_signal=residual,
        metrics=calculate_cancellation_metrics(primary, residual),
    )
