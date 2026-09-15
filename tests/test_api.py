import pytest
from pydantic import ValidationError

from src.api.main import SimulationRequest, simulate


def test_simulate_returns_dominant_frequencies() -> None:
    response = simulate(
        SimulationRequest(
            fundamental_hz=120,
            harmonics=3,
        )
    )

    assert response.dominant_frequencies == pytest.approx([120, 240, 360])
    assert response.simulation is True


def test_simulation_request_rejects_harmonics_above_nyquist() -> None:
    with pytest.raises(ValidationError, match="highest harmonic"):
        SimulationRequest(fundamental_hz=2000, harmonics=2)


def test_simulation_request_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        SimulationRequest.model_validate(
            {
                "fundamental_hz": 120,
                "harmonics": 3,
                "duration_seconds": 1,
            }
        )
