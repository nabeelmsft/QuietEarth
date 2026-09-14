"""FastAPI entry point for the QuietEarth simulation."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.acoustic_model import (
    dominant_frequencies,
    generate_harmonic_signal,
    tonal_reduction_db,
)

app = FastAPI(title="QuietEarth", version="0.1.0")


class SimulationRequest(BaseModel):
    fundamental_hz: float = Field(default=120, gt=0)
    harmonic_count: int = Field(default=3, ge=1)
    duration_seconds: float = Field(default=1, gt=0)
    sample_rate_hz: int = Field(default=8000, gt=0)
    control_enabled: bool = True


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {
        "status": "ok",
        "simulation": True,
        "field_validated": False,
    }


@app.post("/simulate")
def simulate(request: SimulationRequest) -> dict[str, object]:
    source = generate_harmonic_signal(
        fundamental_hz=request.fundamental_hz,
        harmonics=request.harmonic_count,
        duration_seconds=request.duration_seconds,
        sample_rate_hz=request.sample_rate_hz,
    )
    residual = source * (0.1 if request.control_enabled else 1.0)

    return {
        "simulation": True,
        "field_validated": False,
        "control_enabled": request.control_enabled,
        "dominant_frequencies_hz": dominant_frequencies(
            source,
            request.sample_rate_hz,
            request.harmonic_count,
        ),
        "tonal_reduction_db": tonal_reduction_db(source, residual),
    }
