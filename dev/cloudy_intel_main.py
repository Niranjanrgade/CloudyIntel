"""
CloudyIntel - A Multi-Agent, Cyclical Workflow for Validated Cloud Architecture Design

This is the main execution file that brings together all components:
- State management
- Agent hierarchy
- Cyclical workflow
- RAG tools
- Graph compilation and execution
"""

import os
import sys
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cloudy_intel_state import CloudyIntelState, create_initial_state, Phase
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
from cloudy_intel_rag import (
    create_enhanced_architect_agent, create_enhanced_validator_agent, create_enhanced_auditor_agent
)

class CloudyIntel:
    """Main CloudyIntel class that orchestrates the entire workflow."""
    
    def __init__(self, cloud_provider: str = "aws", use_rag: bool = True):
        self.cloud_provider = cloud_provider
        self.use_rag = use_rag
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """Build the complete CloudyIntel graph."""
        from langgraph.graph import StateGraph, START, END
        from langgraph.checkpoint.memory import MemorySaver
        
        # Initialize graph builder
        graph_builder = StateGraph(CloudyIntelState)
        
        # =============================================================================
        # ADD ALL NODES
        # =============================================================================
        
        # Phase 1: Architect Team
        graph_builder.add_node("architect_supervisor", architect_supervisor)
        
        if self.use_rag:
            # Use enhanced agents with RAG
            graph_builder.add_node("compute_architect", create_enhanced_architect_agent("compute_architect", "compute", self.cloud_provider))
            graph_builder.add_node("network_architect", create_enhanced_architect_agent("network_architect", "network", self.cloud_provider))
            graph_builder.add_node("storage_architect", create_enhanced_architect_agent("storage_architect", "storage", self.cloud_provider))
            graph_builder.add_node("database_architect", create_enhanced_architect_agent("database_architect", "database", self.cloud_provider))
        else:
            # Use basic agents
            graph_builder.add_node("compute_architect", compute_architect)
            graph_builder.add_node("network_architect", network_architect)
            graph_builder.add_node("storage_architect", storage_architect)
            graph_builder.add_node("database_architect", database_architect)
        
        # Phase 2: Validator Team
        graph_builder.add_node("validator_supervisor", validator_supervisor)
        
        if self.use_rag:
            # Use enhanced validators with RAG
            graph_builder.add_node("compute_validator", create_enhanced_validator_agent("compute_validator", "compute", self.cloud_provider))
            graph_builder.add_node("network_validator", create_enhanced_validator_agent("network_validator", "network", self.cloud_provider))
            graph_builder.add_node("storage_validator", create_enhanced_validator_agent("storage_validator", "storage", self.cloud_provider))
            graph_builder.add_node("database_validator", create_enhanced_validator_agent("database_validator", "database", self.cloud_provider))
        else:
            # Use basic validators
            graph_builder.add_node("compute_validator", compute_validator)
            graph_builder.add_node("network_validator", network_validator)
            graph_builder.add_node("storage_validator", storage_validator)
            graph_builder.add_node("database_validator", database_validator)
        
        # Phase 3: Pillar Auditor Team
        graph_builder.add_node("pillar_audit_supervisor", pillar_audit_supervisor)
        
        if self.use_rag:
            # Use enhanced auditors with RAG
            graph_builder.add_node("security_auditor", create_enhanced_auditor_agent("security_auditor", "security", self.cloud_provider))
            graph_builder.add_node("cost_auditor", create_enhanced_auditor_agent("cost_auditor", "cost", self.cloud_provider))
            graph_builder.add_node("reliability_auditor", create_enhanced_auditor_agent("reliability_auditor", "reliability", self.cloud_provider))
            graph_builder.add_node("performance_auditor", create_enhanced_auditor_agent("performance_auditor", "performance", self.cloud_provider))
            graph_builder.add_node("operational_excellence_auditor", create_enhanced_auditor_agent("operational_excellence_auditor", "operational_excellence", self.cloud_provider))
        else:
            # Use basic auditors
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
        self.graph = graph_builder.compile(checkpointer=memory)
    
    async def run(self, user_problem: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Run the complete CloudyIntel workflow."""
        print(f"🚀 Starting CloudyIntel for: {user_problem}")
        print(f"☁️  Cloud Provider: {self.cloud_provider.upper()}")
        print(f"🔍 RAG Enabled: {self.use_rag}")
        print(f"🔄 Max Iterations: {max_iterations}")
        print("=" * 60)
        
        # Create initial state
        initial_state = create_initial_state(user_problem, self.cloud_provider)
        
        # Run the graph
        try:
            result = await self.graph.ainvoke(initial_state)
            
            print("\n✅ CloudyIntel completed successfully!")
            print(f"📊 Final Phase: {result['current_phase']}")
            print(f"🔄 Total Iterations: {result['iteration_count']}")
            print(f"🏗️  Architecture Components: {len(result['architecture_components'])}")
            print(f"📝 Validation Feedback: {len(result['validation_feedback'])}")
            print(f"🔍 Audit Feedback: {len(result['audit_feedback'])}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error running CloudyIntel: {str(e)}")
            return {"error": str(e)}
    
    def get_architecture_summary(self, result: Dict[str, Any]) -> str:
        """Get a summary of the final architecture."""
        if "error" in result:
            return f"Error: {result['error']}"
        
        summary = f"""
🏗️  CLOUDYINTEL ARCHITECTURE SUMMARY
{'=' * 50}

📋 User Problem: {result.get('user_problem', 'N/A')}
☁️  Cloud Provider: {result.get('cloud_provider', 'N/A').upper()}
🔄 Iterations: {result.get('iteration_count', 0)}
📊 Final Phase: {result.get('current_phase', 'N/A')}

🏗️  ARCHITECTURE COMPONENTS:
"""
        
        for domain, component in result.get('architecture_components', {}).items():
            summary += f"\n🔧 {domain.upper()}: {component.get('agent', 'N/A')}"
            if 'rag_context' in component:
                summary += " (RAG Enhanced)"
        
        summary += f"""

📝 VALIDATION FEEDBACK:
"""
        for feedback in result.get('validation_feedback', []):
            summary += f"\n• {feedback.get('domain', 'N/A')}: {feedback.get('agent', 'N/A')}"
            if feedback.get('has_errors', False):
                summary += " ⚠️  Has Errors"
            else:
                summary += " ✅ No Errors"
        
        summary += f"""

🔍 AUDIT FEEDBACK:
"""
        for feedback in result.get('audit_feedback', []):
            summary += f"\n• {feedback.get('pillar', 'N/A')}: {feedback.get('agent', 'N/A')}"
            if feedback.get('has_flaws', False):
                summary += " ⚠️  Has Flaws"
            else:
                summary += " ✅ No Flaws"
        
        if result.get('architecture_summary'):
            summary += f"""

📄 FINAL ARCHITECTURE SUMMARY:
{result['architecture_summary']}
"""
        
        return summary

async def main():
    """Main function for running CloudyIntel."""
    # Example usage
    user_problem = "Deploy a scalable e-commerce backend with high availability and security"
    cloud_provider = "aws"  # or "azure"
    use_rag = True  # Enable RAG for enhanced accuracy
    
    # Create CloudyIntel instance
    cloudy_intel = CloudyIntel(cloud_provider=cloud_provider, use_rag=use_rag)
    
    # Run the workflow
    result = await cloudy_intel.run(user_problem, max_iterations=5)
    
    # Get and print summary
    summary = cloudy_intel.get_architecture_summary(result)
    print(summary)
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
