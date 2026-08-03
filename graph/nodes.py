from monitoring.profiler import profile_dataset
from monitoring.drift import detect_drift

from agents.root_cause_agent import analyze_root_cause
from agents.fix_agent import generate_fix
from agents.severity_agent import classify_severity
from utils.logger import api_logger

from db.incidents import save_incident


def profile_node(state):

    api_logger.info("Executing Profile Node")

    profile = profile_dataset(state["dataset_path"])

    api_logger.info("Profile Node completed")

    state["profile"] = profile

    return state

def drift_node(state):

    api_logger.info("Executing Drift Node")

    drift_detected, alerts = detect_drift(state["profile"])

    state["drift_detected"] = drift_detected

    api_logger.info(f"Drift={drift_detected} Alerts={len(alerts)}")

    state["alerts"] = alerts

    return state

def severity_node(state):

    api_logger.info(f"State type: {type(state)}")
    api_logger.info(f"State contents before severity: {state}")

    severity = classify_severity(state["alerts"])
    api_logger.info(f"Severity returned: {severity}")

    try:
        state["severity"] = severity
        api_logger.info("Severity added to state successfully")
    except Exception as e:
        api_logger.exception(f"Failed while updating state: {e}")
        raise

    return state

def root_cause_node(state):

    api_logger.info("Executing Root Cause Node")

    root = analyze_root_cause(state["alerts"])

    state["root_cause"] = root

    api_logger.info("Root Cause Node completed")

    return state

def fix_node(state):

    api_logger.info("Executing Fix Node")

    fix = generate_fix(state["alerts"])

    state["fix"] = fix

    api_logger.info("Fix Node completed")

    return state

def incident_node(state):
    api_logger.info("Executing Incident Node")
    
    try:
        api_logger.info("Saving incident to PostgreSQL")
        save_incident(
            incident_type="Data Drift",
            severity=state["severity"],
            alert="\n".join(state["alerts"]),
            root_cause=state["root_cause"],
            recommended_fix=state["fix"]
        )
        api_logger.info("Incident saved successfully")

    except Exception as e:
        state["error"] = str(e)

    return state