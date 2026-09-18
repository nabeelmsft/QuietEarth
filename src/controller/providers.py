"""Measurement providers for recorded and simulated controller inputs."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol

from .models import MeasurementRequest, MeasurementResult, normalize_phase

EXPERIMENT_003_DATASET = (
    Path(__file__).resolve().parents[2]
    / "validation_data"
    / "experiment_003_physical_tonal_attenuation.json"
)


class MeasurementProvider(Protocol):
    """Source of residual amplitudes consumed by the controller."""

    def measure(self, request: MeasurementRequest) -> MeasurementResult:
        """Return one measured amplitude for the requested control state."""
        ...

    def available_measurement_count(
        self, target_frequency_hz: float, phase_degrees: float
    ) -> int:
        """Return how many independent measurements are available."""
        ...


class LiveMicrophoneMeasurementProvider(MeasurementProvider, Protocol):
    """Future live provider contract; no hardware access is implemented.

    A future implementation will capture a fixed-duration microphone window,
    measure the target bin through ``compute_fft()``, and return the residual
    through ``MeasurementResult``. Synchronized control output and all hardware
    safety interlocks remain separate from this provider contract.
    """


class RecordedMeasurementProvider:
    """Read exact physical measurements from the Experiment 003 dataset."""

    def __init__(self, dataset_path: Path = EXPERIMENT_003_DATASET) -> None:
        with dataset_path.open(encoding="utf-8") as dataset_file:
            dataset: dict[str, Any] = json.load(dataset_file)
        self.metadata: dict[str, Any] = dataset["metadata"]
        self._measurements: list[dict[str, Any]] = dataset["measurements"]
        self._validate_dataset()

    def _validate_dataset(self) -> None:
        for measurement in self._measurements:
            amplitude = measurement["measured_amplitude"]
            if (
                not isinstance(amplitude, (int, float))
                or not math.isfinite(amplitude)
                or amplitude < 0
            ):
                raise ValueError(
                    "recorded measured amplitudes must be finite and non-negative"
                )
            if measurement["data_classification"] != "recorded_physical":
                raise ValueError("recorded dataset contains a non-physical measurement")

    def baseline_amplitude(self, condition: str) -> float:
        """Return an explicitly recorded control condition without synthesis."""
        matches = [
            measurement
            for measurement in self._measurements
            if measurement["condition"] == condition
        ]
        if len(matches) != 1:
            raise LookupError(
                f"expected exactly one recorded measurement for condition {condition!r}"
            )
        return float(matches[0]["measured_amplitude"])

    def _phase_measurements(
        self, target_frequency_hz: float, phase_degrees: float
    ) -> list[dict[str, Any]]:
        normalized = normalize_phase(phase_degrees)
        matches = [
            measurement
            for measurement in self._measurements
            if measurement["control_phase_degrees"] is not None
            and math.isclose(
                float(measurement["target_frequency_hz"]),
                target_frequency_hz,
                abs_tol=1e-9,
            )
            and math.isclose(
                normalize_phase(float(measurement["control_phase_degrees"])),
                normalized,
                abs_tol=1e-9,
            )
        ]
        if not matches:
            raise LookupError(
                "no recorded physical measurement exists for "
                f"{target_frequency_hz:g} Hz at {phase_degrees:g} degrees"
            )
        return matches

    def available_measurement_count(
        self, target_frequency_hz: float, phase_degrees: float
    ) -> int:
        return len(self._phase_measurements(target_frequency_hz, phase_degrees))

    def measure(self, request: MeasurementRequest) -> MeasurementResult:
        measurements = self._phase_measurements(
            request.target_frequency_hz, request.phase_degrees
        )
        trial_match = re.search(r"(\d+)$", request.trial_identifier)
        trial_index = int(trial_match.group(1)) - 1 if trial_match else 0
        if trial_index >= len(measurements):
            raise LookupError(
                f"recorded phase {request.phase_degrees:g} has only "
                f"{len(measurements)} measurement(s); trial "
                f"{request.trial_identifier!r} was requested"
            )
        measurement = measurements[trial_index]
        return MeasurementResult(
            request=request,
            measured_amplitude=measurement["measured_amplitude"],
            measurement_source=measurement["measurement_source"],
            is_physical_recording=True,
            is_simulated=False,
        )


class SimulationMeasurementProvider:
    """Adapt an injected deterministic response function to the provider API."""

    def __init__(
        self,
        measurement_function: Callable[[MeasurementRequest], float],
        source: str = "deterministic simulated acoustic response",
    ) -> None:
        self._measurement_function = measurement_function
        self._source = source

    def available_measurement_count(
        self, target_frequency_hz: float, phase_degrees: float
    ) -> int:
        del target_frequency_hz, phase_degrees
        return 2**31 - 1

    def measure(self, request: MeasurementRequest) -> MeasurementResult:
        amplitude = self._measurement_function(request)
        return MeasurementResult(
            request=request,
            measured_amplitude=amplitude,
            measurement_source=self._source,
            is_physical_recording=False,
            is_simulated=True,
        )
