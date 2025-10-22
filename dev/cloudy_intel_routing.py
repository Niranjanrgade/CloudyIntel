from typing import Dict, Any
from cloudy_intel_state import CloudyIntelState, Phase, check_iteration_limit

def phase_router(state: CloudyIntelState) -> str:
    """
    Routes between the three main phases based on current_phase and quality gates.
    """
    if state["current_phase"] == Phase.GENERATE:
        return "architect_supervisor"
    elif state["current_phase"] == Phase.VALIDATE:
        return "validator_supervisor"
    elif state["current_phase"] == Phase.AUDIT:
        return "pillar_audit_supervisor"
    elif state["current_phase"] == Phase.COMPLETE:
        return "final_presenter"
    else:
        return "architect_supervisor"  # Default fallback

def inner_loop_router(state: CloudyIntelState) -> str:
    """
    Inner loop: Routes back to architects if factual errors exist.
    Routes to audit phase if no factual errors.
    """
    if state["factual_errors_exist"]:
        # Reset for new iteration
        new_state = state.copy()
        new_state["current_phase"] = Phase.GENERATE
        new_state["iteration_count"] += 1
        new_state["validation_feedback"] = []  # Clear for new iteration
        return "architect_supervisor"
    else:
        # Move to audit phase
        new_state = state.copy()
        new_state["current_phase"] = Phase.AUDIT
        return "pillar_audit_supervisor"

def outer_loop_router(state: CloudyIntelState) -> str:
    """
    Outer loop: Routes back to architects if design flaws exist.
    Routes to completion if no design flaws.
    """
    if state["design_flaws_exist"]:
        # Reset for new iteration
        new_state = state.copy()
        new_state["current_phase"] = Phase.GENERATE
        new_state["iteration_count"] += 1
        new_state["audit_feedback"] = []  # Clear for new iteration
        return "architect_supervisor"
    else:
        # Architecture is complete
        new_state = state.copy()
        new_state["current_phase"] = Phase.COMPLETE
        return "final_presenter"

def agent_completion_router(state: CloudyIntelState) -> str:
    """
    Routes based on which agents have completed their tasks.
    """
    if state["current_phase"] == Phase.GENERATE:
        # Check if all architects are done
        required_agents = ["compute_architect", "network_architect", "storage_architect", "database_architect"]
        if all(agent in state["completed_agents"] for agent in required_agents):
            return "move_to_validation"
        else:
            return "continue_generation"
    
    elif state["current_phase"] == Phase.VALIDATE:
        # Check if all validators are done
        required_agents = ["compute_validator", "network_validator", "storage_validator", "database_validator"]
        if all(agent in state["completed_agents"] for agent in required_agents):
            return "evaluate_validation"
        else:
            return "continue_validation"
    
    elif state["current_phase"] == Phase.AUDIT:
        # Check if all auditors are done
        required_agents = ["security_auditor", "cost_auditor", "reliability_auditor", "performance_auditor", "operational_excellence_auditor"]
        if all(agent in state["completed_agents"] for agent in required_agents):
            return "evaluate_audit"
        else:
            return "continue_audit"

def should_continue_looping(state: CloudyIntelState) -> str:
    """Decide whether to continue looping or force completion."""
    if not check_iteration_limit(state):
        return "force_completion"
    elif state["factual_errors_exist"] or state["design_flaws_exist"]:
        return "continue_looping"
    else:
        return "complete"

def evaluate_validation_feedback(state: CloudyIntelState) -> str:
    """Evaluate validation feedback and determine next step."""
    if not state["validation_feedback"]:
        return "move_to_audit"
    
    # Check if any validation feedback indicates errors
    has_errors = any(feedback.get("has_errors", False) for feedback in state["validation_feedback"])
    
    if has_errors:
        # Update state to indicate factual errors exist
        new_state = state.copy()
        new_state["factual_errors_exist"] = True
        return "return_to_architects"
    else:
        return "move_to_audit"

def evaluate_audit_feedback(state: CloudyIntelState) -> str:
    """Evaluate audit feedback and determine next step."""
    if not state["audit_feedback"]:
        return "complete"
    
    # Check if any audit feedback indicates design flaws
    has_flaws = any(feedback.get("has_flaws", False) for feedback in state["audit_feedback"])
    
    if has_flaws:
        # Update state to indicate design flaws exist
        new_state = state.copy()
        new_state["design_flaws_exist"] = True
        return "return_to_architects"
    else:
        return "complete"

def force_completion(state: CloudyIntelState) -> CloudyIntelState:
    """Force completion when iteration limit is reached."""
    new_state = state.copy()
    new_state["current_phase"] = Phase.COMPLETE
    new_state["messages"].append({
        "role": "system",
        "content": "Maximum iterations reached. Forcing completion with current architecture."
    })
    return new_state
