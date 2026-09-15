"""Core acoustic simulation utilities for QuietEarth."""

from .cancellation import (
    CancellationMetrics,
    CancellationResult,
    calculate_cancellation_metrics,
    combine_signals,
    generate_control_signal,
    simulate_ideal_tonal_cancellation,
)
from .metrics import (
    calculate_peak_level,
    calculate_rms,
    calculate_signal_energy,
    tonal_reduction_db,
)
from .propagation import (
    DEFAULT_SPEED_OF_SOUND_M_S,
    PropagatedCancellationResult,
    PropagationPath,
    apply_propagation_delay,
    calculate_delay_samples,
    calculate_propagation_delay,
    describe_propagation_path,
    simulate_propagated_tonal_cancellation,
)
from .signal_generator import generate_harmonic_signal, generate_tone
from .spectral_analysis import compute_fft, find_dominant_frequencies

__all__ = [
    "CancellationMetrics",
    "CancellationResult",
    "DEFAULT_SPEED_OF_SOUND_M_S",
    "PropagatedCancellationResult",
    "PropagationPath",
    "apply_propagation_delay",
    "calculate_cancellation_metrics",
    "calculate_delay_samples",
    "calculate_peak_level",
    "calculate_propagation_delay",
    "calculate_rms",
    "calculate_signal_energy",
    "combine_signals",
    "compute_fft",
    "describe_propagation_path",
    "find_dominant_frequencies",
    "generate_control_signal",
    "generate_harmonic_signal",
    "generate_tone",
    "simulate_ideal_tonal_cancellation",
    "simulate_propagated_tonal_cancellation",
    "tonal_reduction_db",
]
