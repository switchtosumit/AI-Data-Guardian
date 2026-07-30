from typing import TypedDict

class GuardianState(TypedDict):
    """
    A TypedDict representing the state of the Guardian.
    """
    dataset_path: str

    profile: dict

    drift_detected: bool

    alerts: list

    severity: str

    root_cause: str

    fix: str

    incident_id: int

