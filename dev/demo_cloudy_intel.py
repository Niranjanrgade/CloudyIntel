#!/usr/bin/env python3
"""
CloudyIntel Demo Script

This script demonstrates the complete CloudyIntel system with a simple example.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_basic_workflow():
    """Demonstrate basic CloudyIntel workflow."""
    print("🚀 CLOUDYINTEL DEMO")
    print("=" * 50)
    
    try:
        from cloudy_intel_main import CloudyIntel
        
        # Create CloudyIntel instance
        print("📦 Creating CloudyIntel instance...")
        cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=False)
        print("✅ CloudyIntel instance created successfully")
        
        # Define a simple problem
        user_problem = "Deploy a simple web application with a database"
        print(f"\n🎯 User Problem: {user_problem}")
        
        # Run the workflow
        print("\n🔄 Running CloudyIntel workflow...")
        result = cloudy_intel.run(user_problem, max_iterations=2)
        
        # Display results
        print("\n📊 RESULTS:")
        print(f"Phase: {result.get('current_phase', 'N/A')}")
        print(f"Iterations: {result.get('iteration_count', 0)}")
        print(f"Components: {len(result.get('architecture_components', {}))}")
        print(f"Validation Feedback: {len(result.get('validation_feedback', []))}")
        print(f"Audit Feedback: {len(result.get('audit_feedback', []))}")
        
        # Get architecture summary
        summary = cloudy_intel.get_architecture_summary(result)
        print(f"\n📄 ARCHITECTURE SUMMARY:")
        print(summary)
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False

def demo_state_management():
    """Demonstrate state management."""
    print("\n🧪 STATE MANAGEMENT DEMO")
    print("=" * 40)
    
    try:
        from cloudy_intel_state import create_initial_state, Phase
        
        # Create initial state
        state = create_initial_state("Test problem", "aws")
        print(f"✅ Initial state created")
        print(f"   User Problem: {state['user_problem']}")
        print(f"   Cloud Provider: {state['cloud_provider']}")
        print(f"   Current Phase: {state['current_phase']}")
        print(f"   Iteration Count: {state['iteration_count']}")
        
        # Test state updates
        state['current_phase'] = Phase.VALIDATE
        state['iteration_count'] = 1
        print(f"✅ State updated")
        print(f"   New Phase: {state['current_phase']}")
        print(f"   New Iteration: {state['iteration_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ State management demo failed: {str(e)}")
        return False

def demo_agent_hierarchy():
    """Demonstrate agent hierarchy."""
    print("\n🤖 AGENT HIERARCHY DEMO")
    print("=" * 40)
    
    try:
        from cloudy_intel_agents import architect_supervisor, compute_architect
        from cloudy_intel_state import create_initial_state
        
        # Create state
        state = create_initial_state("Test problem", "aws")
        print(f"✅ State created for agent demo")
        
        # Test architect supervisor
        print("📋 Testing Architect Supervisor...")
        result = architect_supervisor(state)
        print(f"   Active Agents: {result.get('active_agents', [])}")
        print(f"   Messages: {len(result.get('messages', []))}")
        
        # Test compute architect
        print("🔧 Testing Compute Architect...")
        result = compute_architect(state)
        print(f"   Architecture Components: {len(result.get('architecture_components', {}))}")
        print(f"   Completed Agents: {result.get('completed_agents', [])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent hierarchy demo failed: {str(e)}")
        return False

def demo_routing_logic():
    """Demonstrate routing logic."""
    print("\n🔄 ROUTING LOGIC DEMO")
    print("=" * 40)
    
    try:
        from cloudy_intel_routing import phase_router, inner_loop_router, outer_loop_router
        from cloudy_intel_state import create_initial_state, Phase
        
        # Create state
        state = create_initial_state("Test problem", "aws")
        print(f"✅ State created for routing demo")
        
        # Test phase router
        print("📊 Testing Phase Router...")
        result = phase_router(state)
        print(f"   Phase Router Result: {result}")
        
        # Test inner loop router
        print("🔄 Testing Inner Loop Router...")
        state['factual_errors_exist'] = True
        result = inner_loop_router(state)
        print(f"   Inner Loop Router Result: {result}")
        
        # Test outer loop router
        print("🔄 Testing Outer Loop Router...")
        state['design_flaws_exist'] = True
        result = outer_loop_router(state)
        print(f"   Outer Loop Router Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Routing logic demo failed: {str(e)}")
        return False

def demo_rag_system():
    """Demonstrate RAG system."""
    print("\n🔍 RAG SYSTEM DEMO")
    print("=" * 40)
    
    try:
        from cloudy_intel_rag import CloudyIntelRAG, create_architect_rag_tools
        
        # Create RAG system
        print("📚 Creating RAG system...")
        rag = CloudyIntelRAG(cloud_provider="aws")
        print(f"✅ RAG system created")
        
        # Test RAG tools
        print("🛠️  Testing RAG tools...")
        tools = create_architect_rag_tools("aws")
        print(f"   Created {len(tools)} RAG tools")
        
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG system demo failed: {str(e)}")
        return False

def main():
    """Run all demos."""
    print("🎮 CLOUDYINTEL COMPLETE DEMO")
    print("=" * 60)
    
    demos = [
        ("State Management", demo_state_management),
        ("Agent Hierarchy", demo_agent_hierarchy),
        ("Routing Logic", demo_routing_logic),
        ("RAG System", demo_rag_system),
        ("Basic Workflow", demo_basic_workflow)
    ]
    
    passed = 0
    total = len(demos)
    
    for demo_name, demo_func in demos:
        print(f"\n🎯 Running {demo_name} Demo...")
        if demo_func():
            print(f"✅ {demo_name} demo completed successfully")
            passed += 1
        else:
            print(f"❌ {demo_name} demo failed")
    
    print(f"\n📊 DEMO RESULTS: {passed}/{total} demos passed")
    
    if passed == total:
        print("🎉 All demos completed successfully! CloudyIntel is working perfectly.")
    else:
        print("⚠️  Some demos failed. Check the output above for details.")
    
    print("\n🚀 CLOUDYINTEL IS READY TO USE!")
    print("=" * 40)
    print("To run CloudyIntel with your own problems:")
    print("1. Set your API keys in .env file")
    print("2. Run: python cloudy_intel_main.py")
    print("3. Or use the examples: python cloudy_intel_examples.py --demo")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
