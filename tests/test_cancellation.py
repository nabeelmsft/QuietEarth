import numpy as np
import pytest

from src.acoustic_model.cancellation import (
    calculate_cancellation_metrics,
    combine_signals,
    generate_control_signal,
    simulate_ideal_tonal_cancellation,
)
from src.acoustic_model.signal_generator import generate_tone


def test_equal_amplitude_180_degree_control_cancels_tone() -> None:
    result = simulate_ideal_tonal_cancellation(
        frequency_hz=120,
        amplitude=1,
        duration_seconds=1,
        sample_rate_hz=8000,
    )

    assert result.residual_signal == pytest.approx(0, abs=1e-12)
    assert result.metrics.rms_after < 1e-12
    assert result.metrics.residual_energy_ratio < 1e-24
    assert result.metrics.reduction_db is None


def test_zero_degree_control_reinforces_tone() -> None:
    primary = generate_tone(120, duration_seconds=1)
    control = generate_control_signal(120, 1, 0, duration_seconds=1)
    residual = combine_signals(primary, control)

    assert residual == pytest.approx(2 * primary)
    assert calculate_cancellation_metrics(primary, residual).rms_after == pytest.approx(
        2 * calculate_cancellation_metrics(primary, primary).rms_before
    )


@pytest.mark.parametrize("phase_offset", [30, 60, 90, 120, 150])
def test_non_180_degree_phase_leaves_measurable_residual(
    phase_offset: float,
) -> None:
    primary = generate_tone(120, duration_seconds=1)
    control = generate_control_signal(120, 1, phase_offset, duration_seconds=1)
    residual = combine_signals(primary, control)

    assert calculate_cancellation_metrics(primary, residual).rms_after > 1e-6


def test_180_degree_control_with_amplitude_mismatch_is_incomplete() -> None:
    primary = generate_tone(120, duration_seconds=1, amplitude=1)
    control = generate_control_signal(120, 0.8, 180, duration_seconds=1)
    residual = combine_signals(primary, control)
    metrics = calculate_cancellation_metrics(primary, residual)

    assert metrics.rms_after == pytest.approx(metrics.rms_before * 0.2)
    assert metrics.residual_energy_ratio == pytest.approx(0.04)
    assert metrics.reduction_db == pytest.approx(13.9794000867)


def test_frequency_mismatch_does_not_sustain_cancellation() -> None:
    primary = generate_tone(120, duration_seconds=1)
    control = generate_control_signal(121, 1, 180, duration_seconds=1)
    residual = combine_signals(primary, control)
    metrics = calculate_cancellation_metrics(primary, residual)

    assert metrics.rms_after > 0.1
    assert metrics.residual_energy_ratio > 0.01


def test_combine_signals_rejects_different_lengths() -> None:
    with pytest.raises(ValueError, match="equal shapes"):
        combine_signals([0, 1], [0])


def test_cancellation_metrics_reject_different_lengths() -> None:
    with pytest.raises(ValueError, match="equal shapes"):
        calculate_cancellation_metrics([0, 1], [0])


def test_generate_control_signal_supports_requested_phase_offsets() -> None:
    for phase_offset in [0, 30, 60, 90, 120, 150, 180]:
        signal = generate_control_signal(120, 1, phase_offset, 0.01)
        assert isinstance(signal, np.ndarray)
        assert np.isfinite(signal).all()
