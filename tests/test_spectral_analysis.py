import pytest

from src.acoustic_model.signal_generator import generate_harmonic_signal, generate_tone
from src.acoustic_model.spectral_analysis import (
    compute_spectrum,
    dominant_frequencies,
)


def test_spectrum_identifies_fundamental_and_harmonics() -> None:
    signal = generate_harmonic_signal(100, 3, 1, 2000)

    peaks = dominant_frequencies(signal, sample_rate_hz=2000, count=3)

    assert peaks == pytest.approx([100, 200, 300])


def test_compute_spectrum_returns_expected_amplitude() -> None:
    signal = generate_tone(100, 1, 2000)
    frequencies, amplitudes = compute_spectrum(signal, sample_rate_hz=2000)

    tone_index = int((frequencies == 100).nonzero()[0][0])
    assert amplitudes[tone_index] == pytest.approx(1.0)
