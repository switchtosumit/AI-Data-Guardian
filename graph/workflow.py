from langgraph.graph import StateGraph, END

from graph.state import GuardianState

from graph.nodes import (
    profile_node,
    drift_node,
    severity_node,
    root_cause_node,
    fix_node,
    incident_node
)

# Define the workflow using the StateGraph
workflow = StateGraph(GuardianState)

# Define the nodes in the workflow
workflow.add_node("profile", profile_node)

workflow.add_node("drift", drift_node)

workflow.add_node("severity", severity_node)

workflow.add_node("root_cause", root_cause_node)

workflow.add_node("fix", fix_node)

workflow.add_node("incident", incident_node)

# Set Entry Point
workflow.set_entry_point("profile")

# Normal Edges
workflow.add_edge("profile", "drift")

# Define function

def route_after_drift(state):

    if state["drift_detected"]:
        return "severity"

    return END

workflow.add_conditional_edges(
    "drift",
    route_after_drift
)

workflow.add_edge("severity", "root_cause")

workflow.add_edge("root_cause", "fix")

workflow.add_edge("fix", "incident")

workflow.add_edge("incident", END)


guardian_graph = workflow.compile()
