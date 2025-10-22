from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from cloudy_intel_state import CloudyIntelState, create_initial_state
from cloudy_intel_agents import (
    architect_supervisor, compute_architect, network_architect, storage_architect, database_architect,
    validator_supervisor, compute_validator, network_validator, storage_validator, database_validator,
    pillar_audit_supervisor, security_auditor, cost_auditor, reliability_auditor, performance_auditor, operational_excellence_auditor,
    final_presenter
)
from cloudy_intel_routing import (
    phase_router, inner_loop_router, outer_loop_router, agent_completion_router,
    evaluate_validation_feedback, evaluate_audit_feedback, force_completion
)

def build_cloudy_intel_graph():
    """Build the complete CloudyIntel graph with all nodes and routing logic."""
    
    # Initialize graph builder
    graph_builder = StateGraph(CloudyIntelState)
    
    # =============================================================================
    # ADD ALL NODES
    # =============================================================================
    
    # Phase 1: Architect Team
    graph_builder.add_node("architect_supervisor", architect_supervisor)
    graph_builder.add_node("compute_architect", compute_architect)
    graph_builder.add_node("network_architect", network_architect)
    graph_builder.add_node("storage_architect", storage_architect)
    graph_builder.add_node("database_architect", database_architect)
    
    # Phase 2: Validator Team
    graph_builder.add_node("validator_supervisor", validator_supervisor)
    graph_builder.add_node("compute_validator", compute_validator)
    graph_builder.add_node("network_validator", network_validator)
    graph_builder.add_node("storage_validator", storage_validator)
    graph_builder.add_node("database_validator", database_validator)
    
    # Phase 3: Pillar Auditor Team
    graph_builder.add_node("pillar_audit_supervisor", pillar_audit_supervisor)
    graph_builder.add_node("security_auditor", security_auditor)
    graph_builder.add_node("cost_auditor", cost_auditor)
    graph_builder.add_node("reliability_auditor", reliability_auditor)
    graph_builder.add_node("performance_auditor", performance_auditor)
    graph_builder.add_node("operational_excellence_auditor", operational_excellence_auditor)
    
    # Final Presenter
    graph_builder.add_node("final_presenter", final_presenter)
    
    # =============================================================================
    # ADD EDGES
    # =============================================================================
    
    # Start with architect supervisor
    graph_builder.add_edge(START, "architect_supervisor")
    
    # Phase 1: Architect team coordination
    graph_builder.add_conditional_edges(
        "architect_supervisor",
        agent_completion_router,
        {
            "continue_generation": "compute_architect",
            "move_to_validation": "validator_supervisor"
        }
    )
    
    # Architect team parallel execution
    graph_builder.add_edge("compute_architect", "network_architect")
    graph_builder.add_edge("network_architect", "storage_architect")
    graph_builder.add_edge("storage_architect", "database_architect")
    
    # After all architects complete, move to validation
    graph_builder.add_conditional_edges(
        "database_architect",
        agent_completion_router,
        {
            "continue_generation": "compute_architect",  # Should not happen
            "move_to_validation": "validator_supervisor"
        }
    )
    
    # Phase 2: Validator team coordination
    graph_builder.add_conditional_edges(
        "validator_supervisor",
        agent_completion_router,
        {
            "continue_validation": "compute_validator",
            "evaluate_validation": "evaluate_validation_feedback"
        }
    )
    
    # Validator team parallel execution
    graph_builder.add_edge("compute_validator", "network_validator")
    graph_builder.add_edge("network_validator", "storage_validator")
    graph_builder.add_edge("storage_validator", "database_validator")
    
    # After all validators complete, evaluate feedback
    graph_builder.add_conditional_edges(
        "database_validator",
        agent_completion_router,
        {
            "continue_validation": "compute_validator",  # Should not happen
            "evaluate_validation": "evaluate_validation_feedback"
        }
    )
    
    # Validation feedback evaluation
    graph_builder.add_conditional_edges(
        "evaluate_validation_feedback",
        evaluate_validation_feedback,
        {
            "return_to_architects": "architect_supervisor",
            "move_to_audit": "pillar_audit_supervisor"
        }
    )
    
    # Phase 3: Pillar auditor team coordination
    graph_builder.add_conditional_edges(
        "pillar_audit_supervisor",
        agent_completion_router,
        {
            "continue_audit": "security_auditor",
            "evaluate_audit": "evaluate_audit_feedback"
        }
    )
    
    # Auditor team parallel execution
    graph_builder.add_edge("security_auditor", "cost_auditor")
    graph_builder.add_edge("cost_auditor", "reliability_auditor")
    graph_builder.add_edge("reliability_auditor", "performance_auditor")
    graph_builder.add_edge("performance_auditor", "operational_excellence_auditor")
    
    # After all auditors complete, evaluate feedback
    graph_builder.add_conditional_edges(
        "operational_excellence_auditor",
        agent_completion_router,
        {
            "continue_audit": "security_auditor",  # Should not happen
            "evaluate_audit": "evaluate_audit_feedback"
        }
    )
    
    # Audit feedback evaluation
    graph_builder.add_conditional_edges(
        "evaluate_audit_feedback",
        evaluate_audit_feedback,
        {
            "return_to_architects": "architect_supervisor",
            "complete": "final_presenter"
        }
    )
    
    # Final presenter
    graph_builder.add_edge("final_presenter", END)
    
    # =============================================================================
    # COMPILE GRAPH
    # =============================================================================
    
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    
    return graph

def create_cloudy_intel_session(user_problem: str, cloud_provider: str = "aws"):
    """Create a new CloudyIntel session."""
    graph = build_cloudy_intel_graph()
    initial_state = create_initial_state(user_problem, cloud_provider)
    
    return graph, initial_state

def run_cloudy_intel(user_problem: str, cloud_provider: str = "aws", max_iterations: int = 5):
    """Run the complete CloudyIntel workflow."""
    graph, initial_state = create_cloudy_intel_session(user_problem, cloud_provider)
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    return result

# Example usage
if __name__ == "__main__":
    # Example usage
    user_problem = "Deploy a scalable e-commerce backend with high availability and security"
    cloud_provider = "aws"
    
    print(f"Starting CloudyIntel for: {user_problem}")
    print(f"Cloud Provider: {cloud_provider}")
    
    result = run_cloudy_intel(user_problem, cloud_provider)
    
    print("\n=== FINAL RESULT ===")
    print(f"Phase: {result['current_phase']}")
    print(f"Iterations: {result['iteration_count']}")
    print(f"Architecture Summary: {result['architecture_summary']}")
