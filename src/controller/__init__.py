"""Autonomous tonal-control search interfaces."""

from .controller import TonalController, calculate_reduction_metrics
from .models import (
    ControllerConfig,
    ControllerReport,
    ControllerState,
    MeasurementMode,
    MeasurementRequest,
    MeasurementResult,
    MeasurementStatistics,
    PhaseEvaluation,
    ReacquisitionDecision,
    ReductionMetrics,
    calculate_measurement_statistics,
    normalize_phase,
)
from .providers import (
    EXPERIMENT_003_DATASET,
    LiveMicrophoneMeasurementProvider,
    MeasurementProvider,
    RecordedMeasurementProvider,
    SimulationMeasurementProvider,
)

__all__ = [
    "EXPERIMENT_003_DATASET",
    "ControllerConfig",
    "ControllerReport",
    "ControllerState",
    "LiveMicrophoneMeasurementProvider",
    "MeasurementMode",
    "MeasurementProvider",
    "MeasurementRequest",
    "MeasurementResult",
    "MeasurementStatistics",
    "PhaseEvaluation",
    "ReacquisitionDecision",
    "RecordedMeasurementProvider",
    "ReductionMetrics",
    "SimulationMeasurementProvider",
    "TonalController",
    "calculate_measurement_statistics",
    "calculate_reduction_metrics",
    "normalize_phase",
]
