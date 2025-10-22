from typing import Dict, Any, List
from cloudy_intel_state import CloudyIntelState, Phase, check_iteration_limit

def determine_relevant_agents(user_problem: str) -> List[str]:
    """
    Intelligently determine which architect agents are relevant based on the user's problem.
    This prevents unnecessary token usage by only running relevant agents.
    """
    problem_lower = user_problem.lower()
    relevant_agents = []
    
    # Storage-related keywords
    storage_keywords = [
        'store', 'storage', 'data', 'file', 'backup', 'archive', 's3', 'bucket',
        'volume', 'disk', 'nas', 'filesystem', 'object storage', 'block storage',
        'retention', 'lifecycle', 'cold storage', 'hot storage'
    ]
    
    # Database-related keywords  
    database_keywords = [
        'database', 'db', 'sql', 'nosql', 'query', 'table', 'index', 'transaction',
        'rds', 'dynamodb', 'postgres', 'mysql', 'oracle', 'sql server', 'mongodb',
        'redis', 'cache', 'data warehouse', 'analytics', 'reporting'
    ]
    
    # Compute-related keywords
    compute_keywords = [
        'compute', 'server', 'instance', 'cpu', 'memory', 'processing', 'application',
        'api', 'service', 'microservice', 'container', 'docker', 'kubernetes',
        'lambda', 'function', 'serverless', 'ec2', 'ecs', 'eks', 'fargate'
    ]
    
    # Network-related keywords
    network_keywords = [
        'network', 'vpc', 'subnet', 'security group', 'load balancer', 'dns',
        'cdn', 'cloudfront', 'route53', 'vpn', 'direct connect', 'nat',
        'firewall', 'routing', 'bandwidth', 'latency', 'connectivity'
    ]
    
    # Check for storage relevance
    if any(keyword in problem_lower for keyword in storage_keywords):
        relevant_agents.append("storage_architect")
    
    # Check for database relevance
    if any(keyword in problem_lower for keyword in database_keywords):
        relevant_agents.append("database_architect")
    
    # Check for compute relevance
    if any(keyword in problem_lower for keyword in compute_keywords):
        relevant_agents.append("compute_architect")
    
    # Check for network relevance
    if any(keyword in problem_lower for keyword in network_keywords):
        relevant_agents.append("network_architect")
    
    # If no specific domains are detected, default to all agents for comprehensive coverage
    if not relevant_agents:
        relevant_agents = ["compute_architect", "network_architect", "storage_architect", "database_architect"]
    
    return relevant_agents

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
    Uses intelligent filtering to only require relevant agents.
    """
    if state["current_phase"] == Phase.GENERATE:
        # Determine which agents are actually needed based on the problem
        required_agents = determine_relevant_agents(state["user_problem"])
        
        # Check if all relevant architects are done
        if all(agent in state["completed_agents"] for agent in required_agents):
            return "move_to_validation"
        else:
            return "continue_generation"
    
    elif state["current_phase"] == Phase.VALIDATE:
        # Determine which validators are needed based on the original problem
        relevant_architects = determine_relevant_agents(state["user_problem"])
        required_agents = [agent.replace("_architect", "_validator") for agent in relevant_architects]
        
        if all(agent in state["completed_agents"] for agent in required_agents):
            return "evaluate_validation"
        else:
            return "continue_validation"
    
    elif state["current_phase"] == Phase.AUDIT:
        # All auditors are always needed for comprehensive quality assessment
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
