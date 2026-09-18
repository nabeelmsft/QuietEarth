from experiments.experiment_004_controller_phase_search import run_experiment
from src.controller import ControllerState


def test_experiment_004_returns_structured_maintain_and_reacquisition_results() -> None:
    report, reacquisition = run_experiment()

    assert report.selected_normalized_phase_degrees == 45
    assert report.controller_state == ControllerState.MAINTAIN
    assert report.model_dump(mode="json")["scientific_validation_labels"][
        "datacenter_field_validated"
    ] is False
    assert reacquisition.reacquisition_required
    assert reacquisition.resulting_state == ControllerState.REACQUIRE
