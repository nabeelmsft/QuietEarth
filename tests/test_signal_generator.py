import numpy as np
import pytest

from src.acoustic_model.signal_generator import generate_tonal_signal


def test_generate_tonal_signal_is_deterministic() -> None:
    time, signal = generate_tonal_signal(
        fundamental_hz=100,
        harmonic_count=2,
        duration_seconds=1,
        sample_rate_hz=1000,
    )

    assert time.shape == signal.shape == (1000,)
    assert signal[0] == pytest.approx(0)
    assert np.isfinite(signal).all()


def test_generate_tonal_signal_rejects_frequency_above_nyquist() -> None:
    with pytest.raises(ValueError, match="Nyquist"):
        generate_tonal_signal(300, 2, 1, 1000)
