"""Core acoustic simulation utilities for QuietEarth."""

from .metrics import (
    calculate_peak_level,
    calculate_rms,
    calculate_signal_energy,
    tonal_reduction_db,
)
from .signal_generator import generate_harmonic_signal, generate_tone
from .spectral_analysis import compute_fft, find_dominant_frequencies

__all__ = [
    "calculate_peak_level",
    "calculate_rms",
    "calculate_signal_energy",
    "compute_fft",
    "find_dominant_frequencies",
    "generate_harmonic_signal",
    "generate_tone",
    "tonal_reduction_db",
]
