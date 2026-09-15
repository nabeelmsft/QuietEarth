import numpy as np
import pytest

from src.acoustic_model.signal_generator import (
    generate_harmonic_signal,
    generate_tone,
)


def test_generate_tone_returns_expected_sine_wave() -> None:
    signal = generate_tone(2, duration_seconds=1, sample_rate_hz=8, amplitude=0.5)

    assert isinstance(signal, np.ndarray)
    assert signal.dtype == np.float64
    assert signal == pytest.approx([0, 0.5, 0, -0.5, 0, 0.5, 0, -0.5])


def test_generate_tone_uses_default_sample_rate() -> None:
    signal = generate_tone(120, duration_seconds=0.5)

    assert signal.shape == (4000,)


def test_generate_tone_supports_phase_offset() -> None:
    signal = generate_tone(
        1,
        duration_seconds=0.25,
        sample_rate_hz=4,
        phase_degrees=90,
    )

    assert signal == pytest.approx([1])


def test_generate_tone_rejects_frequency_at_nyquist() -> None:
    with pytest.raises(ValueError, match="Nyquist"):
        generate_tone(500, duration_seconds=1, sample_rate_hz=1000)


def test_generate_harmonic_signal_combines_expected_tones() -> None:
    signal = generate_harmonic_signal(
        fundamental_hz=120,
        harmonics=3,
        duration_seconds=1,
        sample_rate_hz=1200,
    )
    time = np.arange(1200) / 1200
    expected = (
        np.sin(2 * np.pi * 120 * time)
        + np.sin(2 * np.pi * 240 * time) / 2
        + np.sin(2 * np.pi * 360 * time) / 3
    )

    assert isinstance(signal, np.ndarray)
    assert signal == pytest.approx(expected)


def test_generate_harmonic_signal_rejects_non_integer_harmonics() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        generate_harmonic_signal(120, harmonics=2.5)  # type: ignore[arg-type]
