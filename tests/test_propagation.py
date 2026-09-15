import numpy as np
import pytest

from src.acoustic_model.propagation import (
    apply_propagation_delay,
    calculate_delay_samples,
    simulate_propagated_tonal_cancellation,
)

FREQUENCY_HZ = 120.0
SAMPLE_RATE_HZ = 8000
SPEED_OF_SOUND_M_S = 343.0
PRIMARY_DISTANCE_M = 1.0
CONTROL_DISTANCE_M = (
    PRIMARY_DISTANCE_M + SPEED_OF_SOUND_M_S / (4 * FREQUENCY_HZ)
)


def test_zero_distance_produces_no_delay() -> None:
    signal = np.array([0.0, 1.0, -0.5])

    delayed = apply_propagation_delay(signal, 0, SAMPLE_RATE_HZ)

    assert delayed == pytest.approx(signal)
    assert delayed is not signal


def test_known_distance_produces_expected_sample_delay() -> None:
    signal = np.zeros(16)
    signal[0] = 1
    distance_m = SPEED_OF_SOUND_M_S * 0.001

    delayed = apply_propagation_delay(
        signal,
        distance_m,
        SAMPLE_RATE_HZ,
        SPEED_OF_SOUND_M_S,
    )

    assert calculate_delay_samples(
        distance_m,
        SAMPLE_RATE_HZ,
        SPEED_OF_SOUND_M_S,
    ) == 8
    assert delayed[8] == pytest.approx(1)
    assert np.count_nonzero(delayed) == 1


def test_delayed_samples_do_not_wrap_to_signal_start() -> None:
    signal = np.array([0.0, 0.0, 0.0, 1.0])
    one_sample_distance_m = SPEED_OF_SOUND_M_S / SAMPLE_RATE_HZ

    delayed = apply_propagation_delay(
        signal,
        one_sample_distance_m,
        SAMPLE_RATE_HZ,
        SPEED_OF_SOUND_M_S,
    )

    assert delayed == pytest.approx([0, 0, 0, 0])


def test_equal_paths_preserve_ideal_cancellation() -> None:
    result = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=PRIMARY_DISTANCE_M,
        compensation_enabled=False,
        duration_seconds=1,
        sample_rate_hz=SAMPLE_RATE_HZ,
    )

    assert result.metrics.rms_after < 1e-12
    assert result.metrics.reduction_db is None
    assert result.effective_phase_difference_degrees == pytest.approx(180)


def test_mismatched_paths_degrade_uncompensated_cancellation() -> None:
    equal_paths = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=PRIMARY_DISTANCE_M,
        compensation_enabled=False,
        duration_seconds=1,
        sample_rate_hz=SAMPLE_RATE_HZ,
    )
    mismatched_paths = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=CONTROL_DISTANCE_M,
        compensation_enabled=False,
        duration_seconds=1,
        sample_rate_hz=SAMPLE_RATE_HZ,
    )

    assert mismatched_paths.metrics.rms_after > 0.5
    assert (
        mismatched_paths.metrics.residual_energy_ratio
        > equal_paths.metrics.residual_energy_ratio
    )


def test_propagation_compensation_improves_mismatched_geometry() -> None:
    uncompensated = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=CONTROL_DISTANCE_M,
        compensation_enabled=False,
        duration_seconds=1,
        sample_rate_hz=SAMPLE_RATE_HZ,
    )
    compensated = simulate_propagated_tonal_cancellation(
        frequency_hz=FREQUENCY_HZ,
        primary_distance_m=PRIMARY_DISTANCE_M,
        control_distance_m=CONTROL_DISTANCE_M,
        compensation_enabled=True,
        duration_seconds=1,
        sample_rate_hz=SAMPLE_RATE_HZ,
    )

    assert compensated.metrics.rms_after < uncompensated.metrics.rms_after
    assert (
        compensated.metrics.residual_energy_ratio
        < uncompensated.metrics.residual_energy_ratio * 0.01
    )
    assert compensated.effective_phase_difference_degrees == pytest.approx(180)
