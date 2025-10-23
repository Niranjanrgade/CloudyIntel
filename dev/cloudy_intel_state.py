from typing import TypedDict, Annotated, List, Dict, Any, Optional
from langgraph.graph import add_messages
from enum import Enum
from datetime import datetime
import uuid

class Phase(str, Enum):
    GENERATE = "generate"
    VALIDATE = "validate" 
    AUDIT = "audit"
    COMPLETE = "complete"

class CloudyIntelState(TypedDict):
    # Core workflow state
    messages: Annotated[List, add_messages]
    user_problem: str
    current_phase: Phase
    iteration_count: int
    
    # Task decomposition
    decomposed_tasks: Dict[str, Dict[str, Any]]  # domain -> task details
    task_assignments: Dict[str, str]  # domain -> assigned task description
    
    # Architecture components
    proposed_architecture: Dict[str, Any]
    architecture_components: Dict[str, Dict[str, Any]]  # domain -> component details
    
    # Feedback systems
    validation_feedback: List[Dict[str, Any]]
    audit_feedback: List[Dict[str, Any]]
    
    # Agent coordination
    active_agents: List[str]
    completed_agents: List[str]
    
    # Quality gates
    factual_errors_exist: bool
    design_flaws_exist: bool
    
    # Final output
    final_architecture: Optional[Dict[str, Any]]
    architecture_summary: Optional[str]
    
    # Metadata
    cloud_provider: str  # "aws" or "azure"
    timestamp: str
    session_id: str

def create_initial_state(user_problem: str, cloud_provider: str = "aws") -> CloudyIntelState:
    """Create initial state for CloudyIntel workflow."""
    return CloudyIntelState(
        messages=[],
        user_problem=user_problem,
        current_phase=Phase.GENERATE,
        iteration_count=0,
        decomposed_tasks={},
        task_assignments={},
        proposed_architecture={},
        architecture_components={},
        validation_feedback=[],
        audit_feedback=[],
        active_agents=[],
        completed_agents=[],
        factual_errors_exist=False,
        design_flaws_exist=False,
        final_architecture=None,
        architecture_summary=None,
        cloud_provider=cloud_provider,
        timestamp=datetime.now().isoformat(),
        session_id=str(uuid.uuid4())
    )

def update_validation_feedback(state: CloudyIntelState, feedback: List[Dict[str, Any]]) -> CloudyIntelState:
    """Update validation feedback and set factual_errors_exist flag."""
    new_state = state.copy()
    new_state["validation_feedback"] = feedback
    new_state["factual_errors_exist"] = len(feedback) > 0
    return new_state

def update_audit_feedback(state: CloudyIntelState, feedback: List[Dict[str, Any]]) -> CloudyIntelState:
    """Update audit feedback and set design_flaws_exist flag."""
    new_state = state.copy()
    new_state["audit_feedback"] = feedback
    new_state["design_flaws_exist"] = len(feedback) > 0
    return new_state

def mark_agent_complete(state: CloudyIntelState, agent_name: str) -> CloudyIntelState:
    """Mark an agent as completed."""
    new_state = state.copy()
    if agent_name not in new_state["completed_agents"]:
        new_state["completed_agents"].append(agent_name)
    return new_state

def check_iteration_limit(state: CloudyIntelState, max_iterations: int = 5) -> bool:
    """Prevent infinite loops."""
    return state["iteration_count"] < max_iterations
