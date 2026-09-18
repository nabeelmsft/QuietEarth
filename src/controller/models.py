"""Validated data models for autonomous tonal-control state search."""

from __future__ import annotations

import math
from enum import StrEnum
from statistics import fmean, median, pstdev

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MeasurementMode(StrEnum):
    """Supported measurement-provider modes."""

    RECORDED = "recorded"
    SIMULATED = "simulated"
    LIVE = "live"


class ControllerState(StrEnum):
    """Conceptual states used by the controller MVP."""

    SEARCH = "SEARCH"
    VERIFY = "VERIFY"
    MAINTAIN = "MAINTAIN"
    REACQUIRE = "REACQUIRE"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"


def normalize_phase(phase_degrees: float) -> float:
    """Normalize a finite phase to the half-open interval [0, 360)."""
    if not math.isfinite(phase_degrees):
        raise ValueError("phase must be finite")
    normalized = phase_degrees % 360.0
    return 0.0 if math.isclose(normalized, 360.0, abs_tol=1e-12) else normalized


def normalized_absolute_phase(phase_degrees: float) -> float:
    """Return the shortest absolute angular distance from zero degrees."""
    normalized = normalize_phase(phase_degrees)
    return min(normalized, 360.0 - normalized)


class ControllerConfig(BaseModel):
    """Validated settings for one controller search and verification cycle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    target_frequency_hz: float = Field(gt=0)
    candidate_phases_degrees: list[float] = Field(min_length=1)
    candidate_control_amplitude: float = Field(ge=0)
    measurement_duration_seconds: float = Field(gt=0)
    acoustic_settling_duration_seconds: float = Field(ge=0)
    measurements_per_phase: int = Field(gt=0)
    verification_trials: int = Field(gt=0)
    baseline_amplitude: float = Field(gt=0)
    minimum_required_reduction_percent: float = Field(ge=0, le=100)
    reacquisition_threshold: float = Field(ge=0)
    measurement_mode: MeasurementMode
    numerical_floor: float = Field(gt=0)
    selection_tolerance: float = Field(default=1e-9, ge=0)

    @model_validator(mode="after")
    def validate_finite_values_and_phases(self) -> "ControllerConfig":
        finite_values = (
            self.target_frequency_hz,
            self.candidate_control_amplitude,
            self.measurement_duration_seconds,
            self.acoustic_settling_duration_seconds,
            self.baseline_amplitude,
            self.minimum_required_reduction_percent,
            self.reacquisition_threshold,
            self.numerical_floor,
            self.selection_tolerance,
        )
        if not all(math.isfinite(value) for value in finite_values):
            raise ValueError("controller numeric values must be finite")

        normalized = [normalize_phase(phase) for phase in self.candidate_phases_degrees]
        if len(set(normalized)) != len(normalized):
            raise ValueError("candidate phases must be unique after normalization")
        return self


class MeasurementRequest(BaseModel):
    """One residual-amplitude measurement requested by the controller."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    target_frequency_hz: float = Field(gt=0)
    phase_degrees: float
    control_amplitude: float = Field(ge=0)
    trial_identifier: str = Field(min_length=1)
    measurement_duration_seconds: float = Field(gt=0)
    acoustic_settling_duration_seconds: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_finite_values(self) -> "MeasurementRequest":
        values = (
            self.target_frequency_hz,
            self.phase_degrees,
            self.control_amplitude,
            self.measurement_duration_seconds,
            self.acoustic_settling_duration_seconds,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("measurement request values must be finite")
        return self


class MeasurementResult(BaseModel):
    """A provider result with explicit scientific-provenance labels."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    request: MeasurementRequest
    measured_amplitude: float = Field(ge=0)
    measurement_source: str = Field(min_length=1)
    is_physical_recording: bool
    is_simulated: bool

    @model_validator(mode="after")
    def validate_provenance(self) -> "MeasurementResult":
        if not math.isfinite(self.measured_amplitude):
            raise ValueError("measured amplitude must be finite")
        if self.is_physical_recording == self.is_simulated:
            raise ValueError(
                "measurement must be labeled as exactly one of physical or simulated"
            )
        return self


class MeasurementStatistics(BaseModel):
    """Aggregate statistics for repeated amplitude measurements."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    measured_amplitudes: list[float]
    mean_amplitude: float
    median_amplitude: float
    minimum_amplitude: float
    maximum_amplitude: float
    standard_deviation: float
    measurement_count: int


def calculate_measurement_statistics(
    measured_amplitudes: list[float],
) -> MeasurementStatistics:
    """Aggregate non-negative, finite amplitudes using population deviation."""
    if not measured_amplitudes:
        raise ValueError("at least one measured amplitude is required")
    if any(
        not math.isfinite(amplitude) or amplitude < 0
        for amplitude in measured_amplitudes
    ):
        raise ValueError("measured amplitudes must be finite and non-negative")
    return MeasurementStatistics(
        measured_amplitudes=measured_amplitudes,
        mean_amplitude=fmean(measured_amplitudes),
        median_amplitude=median(measured_amplitudes),
        minimum_amplitude=min(measured_amplitudes),
        maximum_amplitude=max(measured_amplitudes),
        standard_deviation=pstdev(measured_amplitudes),
        measurement_count=len(measured_amplitudes),
    )


class PhaseEvaluation(BaseModel):
    """Search measurements and statistics for one candidate phase."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    display_phase_degrees: float
    normalized_phase_degrees: float
    statistics: MeasurementStatistics
    measurement_source: str
    is_physical_recording: bool
    is_simulated: bool
    available_verification_measurements: int = Field(ge=0)


class ReductionMetrics(BaseModel):
    """Amplitude-ratio metrics relative to a control-disabled baseline."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    baseline_amplitude: float
    selected_residual_amplitude: float
    effective_residual_amplitude: float
    absolute_amplitude_reduction: float
    residual_amplitude_ratio: float
    percentage_amplitude_reduction: float
    amplitude_ratio_reduction_db: float


class ReinforcingConditionImprovement(BaseModel):
    """Improvement of the selected state relative to a reinforcing state."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    reinforcing_phase_degrees: float
    reinforcing_amplitude: float
    absolute_amplitude_reduction: float
    percentage_amplitude_reduction: float
    amplitude_ratio_reduction_db: float


class ReacquisitionDecision(BaseModel):
    """Threshold decision for a later MAINTAIN-state residual."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    measured_amplitude: float
    threshold: float
    reacquisition_required: bool
    resulting_state: ControllerState


class ControllerReport(BaseModel):
    """Transparent structured result from a complete controller cycle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    target_frequency_hz: float
    measurement_mode: MeasurementMode
    baseline_amplitude: float
    phase_evaluations: list[PhaseEvaluation]
    selected_display_phase_degrees: float
    selected_normalized_phase_degrees: float
    verification: MeasurementStatistics
    reduction: ReductionMetrics
    reinforcing_condition_improvement: ReinforcingConditionImprovement | None
    controller_state: ControllerState
    minimum_required_reduction_percent: float
    scientific_validation_labels: dict[str, bool | str]
