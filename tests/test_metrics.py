from collections.abc import Callable

import numpy as np
import pytest
from numpy.typing import ArrayLike

from src.acoustic_model.metrics import (
    calculate_peak_level,
    calculate_rms,
    calculate_signal_energy,
    tonal_reduction_db,
)


def test_calculate_peak_level_uses_absolute_sample_value() -> None:
    assert calculate_peak_level([0.25, -0.75, 0.5]) == pytest.approx(0.75)


def test_calculate_rms_for_sine_wave() -> None:
    time = np.arange(8000) / 8000
    signal = np.sin(2 * np.pi * 120 * time)

    assert calculate_rms(signal) == pytest.approx(1 / np.sqrt(2))


def test_calculate_signal_energy_sums_squared_samples() -> None:
    assert calculate_signal_energy([1, -2, 3]) == pytest.approx(14)


@pytest.mark.parametrize(
    "metric",
    [calculate_peak_level, calculate_rms, calculate_signal_energy],
)
def test_metrics_reject_empty_signals(
    metric: Callable[[ArrayLike], float],
) -> None:
    with pytest.raises(ValueError, match="non-empty"):
        metric([])


def test_tonal_reduction_db_uses_rms() -> None:
    reference = np.ones(100)
    residual = reference * 0.1

    assert tonal_reduction_db(reference, residual) == pytest.approx(20)
