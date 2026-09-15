"""Deterministic propagation-delay model for idealized acoustic signals."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .cancellation import (
    CancellationMetrics,
    calculate_cancellation_metrics,
    combine_signals,
    generate_control_signal,
)
from .signal_generator import generate_tone

DEFAULT_SPEED_OF_SOUND_M_S = 343.0


@dataclass(frozen=True)
class PropagationPath:
    """Distance and discrete delay applied to one simulated acoustic path."""

    distance_m: float
    delay_seconds: float
    delay_samples: int


@dataclass(frozen=True)
class PropagatedCancellationResult:
    """Signals, path details, and metrics for one propagation scenario."""

    primary_path: PropagationPath
    control_path: PropagationPath
    compensation_enabled: bool
    control_phase_offset_degrees: float
    effective_phase_difference_degrees: float
    received_primary: NDArray[np.float64]
    received_control: NDArray[np.float64]
    residual_signal: NDArray[np.float64]
    metrics: CancellationMetrics


def calculate_propagation_delay(
    distance_m: float,
    speed_of_sound_m_s: float = DEFAULT_SPEED_OF_SOUND_M_S,
) -> float:
    """Calculate propagation time while keeping sound speed configurable."""
    if not np.isfinite(distance_m) or distance_m < 0:
        raise ValueError("distance_m must be finite and non-negative")
    if not np.isfinite(speed_of_sound_m_s) or speed_of_sound_m_s <= 0:
        raise ValueError("speed_of_sound_m_s must be finite and positive")
    return distance_m / speed_of_sound_m_s


def calculate_delay_samples(
    distance_m: float,
    sample_rate_hz: int,
    speed_of_sound_m_s: float = DEFAULT_SPEED_OF_SOUND_M_S,
) -> int:
    """Convert propagation time to the nearest whole-sample delay."""
    if (
        isinstance(sample_rate_hz, bool)
        or not isinstance(sample_rate_hz, int)
        or sample_rate_hz <= 0
    ):
        raise ValueError("sample_rate_hz must be a positive integer")
    delay_seconds = calculate_propagation_delay(distance_m, speed_of_sound_m_s)
    return int(np.floor(delay_seconds * sample_rate_hz + 0.5))


def describe_propagation_path(
    distance_m: float,
    sample_rate_hz: int,
    speed_of_sound_m_s: float = DEFAULT_SPEED_OF_SOUND_M_S,
) -> PropagationPath:
    """Describe the physical and discrete delays for a propagation path."""
    return PropagationPath(
        distance_m=distance_m,
        delay_seconds=calculate_propagation_delay(
            distance_m,
            speed_of_sound_m_s,
        ),
        delay_samples=calculate_delay_samples(
            distance_m,
            sample_rate_hz,
            speed_of_sound_m_s,
        ),
    )


def apply_propagation_delay(
    signal: ArrayLike,
    distance_m: float,
    sample_rate_hz: int,
    speed_of_sound_m_s: float = DEFAULT_SPEED_OF_SOUND_M_S,
) -> NDArray[np.float64]:
    """Delay a signal with zero padding and truncation, preserving its length."""
    samples = np.asarray(signal, dtype=np.float64)
    if samples.ndim != 1 or samples.size == 0:
        raise ValueError("signal must be a non-empty one-dimensional sequence")
    if not np.isfinite(samples).all():
        raise ValueError("signal must contain only finite values")

    delay_samples = calculate_delay_samples(
        distance_m,
        sample_rate_hz,
        speed_of_sound_m_s,
    )
    delayed = np.zeros_like(samples)
    if delay_samples == 0:
        delayed[:] = samples
    elif delay_samples < samples.size:
        delayed[delay_samples:] = samples[:-delay_samples]
    return delayed


def simulate_propagated_tonal_cancellation(
    *,
    frequency_hz: float,
    primary_distance_m: float,
    control_distance_m: float,
    compensation_enabled: bool,
    amplitude: float = 1.0,
    duration_seconds: float = 5.0,
    sample_rate_hz: int = 8000,
    speed_of_sound_m_s: float = DEFAULT_SPEED_OF_SOUND_M_S,
) -> PropagatedCancellationResult:
    """Simulate two delayed paths meeting at one acoustic observation point."""
    primary_path = describe_propagation_path(
        primary_distance_m,
        sample_rate_hz,
        speed_of_sound_m_s,
    )
    control_path = describe_propagation_path(
        control_distance_m,
        sample_rate_hz,
        speed_of_sound_m_s,
    )
    applied_delay_difference_seconds = (
        control_path.delay_samples - primary_path.delay_samples
    ) / sample_rate_hz
    compensation_degrees = (
        360.0 * frequency_hz * applied_delay_difference_seconds
        if compensation_enabled
        else 0.0
    )
    control_phase_offset_degrees = 180.0 + compensation_degrees

    primary = generate_tone(
        frequency_hz=frequency_hz,
        amplitude=amplitude,
        duration_seconds=duration_seconds,
        sample_rate_hz=sample_rate_hz,
    )
    control = generate_control_signal(
        frequency_hz=frequency_hz,
        amplitude=amplitude,
        phase_offset_degrees=control_phase_offset_degrees,
        duration_seconds=duration_seconds,
        sample_rate_hz=sample_rate_hz,
    )
    received_primary = apply_propagation_delay(
        primary,
        primary_distance_m,
        sample_rate_hz,
        speed_of_sound_m_s,
    )
    received_control = apply_propagation_delay(
        control,
        control_distance_m,
        sample_rate_hz,
        speed_of_sound_m_s,
    )
    residual = combine_signals(received_primary, received_control)
    effective_phase_difference_degrees = (
        control_phase_offset_degrees
        - 360.0 * frequency_hz * applied_delay_difference_seconds
    ) % 360.0

    return PropagatedCancellationResult(
        primary_path=primary_path,
        control_path=control_path,
        compensation_enabled=compensation_enabled,
        control_phase_offset_degrees=control_phase_offset_degrees,
        effective_phase_difference_degrees=effective_phase_difference_degrees,
        received_primary=received_primary,
        received_control=received_control,
        residual_signal=residual,
        metrics=calculate_cancellation_metrics(received_primary, residual),
    )
