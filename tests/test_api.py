import pytest

from src.api.main import SimulationRequest, simulate


def test_simulate_returns_source_signal_metrics() -> None:
    response = simulate(
        SimulationRequest(
            fundamental_hz=120,
            harmonic_count=1,
            duration_seconds=1,
            sample_rate_hz=8000,
            control_enabled=False,
        )
    )

    assert response["peak_level"] == pytest.approx(1)
    assert response["rms"] == pytest.approx(1 / 2**0.5)
    assert response["signal_energy"] == pytest.approx(4000)
