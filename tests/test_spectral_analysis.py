import pytest

from src.acoustic_model.signal_generator import generate_harmonic_signal, generate_tone
from src.acoustic_model.spectral_analysis import (
    compute_fft,
    find_dominant_frequencies,
)


def test_find_dominant_frequencies_detects_120_hz_tone() -> None:
    signal = generate_tone(120, duration_seconds=5, sample_rate_hz=8000)

    peaks = find_dominant_frequencies(signal, sample_rate_hz=8000, top_n=1)

    assert peaks[0] == pytest.approx(120, abs=0.1)


def test_find_dominant_frequencies_identifies_harmonics() -> None:
    signal = generate_harmonic_signal(120, 3, 1, 2000)

    peaks = find_dominant_frequencies(signal, sample_rate_hz=2000, top_n=3)

    assert peaks == pytest.approx([120, 240, 360])


def test_compute_fft_returns_expected_amplitude() -> None:
    signal = generate_tone(100, 1, 2000)
    frequencies, amplitudes = compute_fft(signal, sample_rate_hz=2000)

    tone_index = int((frequencies == 100).nonzero()[0][0])
    assert amplitudes[tone_index] == pytest.approx(1.0)


def test_find_dominant_frequencies_rejects_invalid_top_n() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        find_dominant_frequencies([0, 1], sample_rate_hz=8000, top_n=0)
