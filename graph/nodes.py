from monitoring.profiler import profile_dataset
from monitoring.drift import detect_drift

from agents.root_cause_agent import analyze_root_cause
from agents.fix_agent import generate_fix
from agents.severity_agent import classify_severity

from db.incidents import save_incident


def profile_node(state):

    profile = profile_dataset(state["dataset_path"])

    state["profile"] = profile

    return state

def drift_node(state):

    drift_detected, alerts = detect_drift(state["profile"])

    state["drift_detected"] = drift_detected

    state["alerts"] = alerts

    return state

def severity_node(state):

    severity = classify_severity(state["alerts"])

    state["severity"] = severity

    return state

def root_cause_node(state):

    root = analyze_root_cause(state["alerts"])

    state["root_cause"] = root

    return state

def fix_node(state):

    fix = generate_fix(state["alerts"])

    state["fix"] = fix

    return state

def incident_node(state):

    incident_id = save_incident(

        state["alerts"],

        state["severity"],

        state["root_cause"],

        state["fix"]

    )

    state["incident_id"] = incident_id

    return state