"""FastAPI entry point for the QuietEarth simulation."""

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.acoustic_model import (
    find_dominant_frequencies,
    generate_harmonic_signal,
)

app = FastAPI(title="QuietEarth", version="0.1.0")

SAMPLE_RATE_HZ = 8000


class SimulationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fundamental_hz: float = Field(gt=0)
    harmonics: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_highest_harmonic(self) -> "SimulationRequest":
        if self.fundamental_hz * self.harmonics >= SAMPLE_RATE_HZ / 2:
            raise ValueError("highest harmonic must be below 4000 Hz")
        return self


class SimulationResponse(BaseModel):
    dominant_frequencies: list[float]
    simulation: bool


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {
        "status": "ok",
        "simulation": True,
        "field_validated": False,
    }


@app.post("/simulate", response_model=SimulationResponse)
def simulate(request: SimulationRequest) -> SimulationResponse:
    source = generate_harmonic_signal(
        fundamental_hz=request.fundamental_hz,
        harmonics=request.harmonics,
        sample_rate_hz=SAMPLE_RATE_HZ,
    )

    return SimulationResponse(
        dominant_frequencies=find_dominant_frequencies(
            source,
            SAMPLE_RATE_HZ,
            top_n=request.harmonics,
        ),
        simulation=True,
    )
