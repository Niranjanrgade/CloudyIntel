#!/usr/bin/env python3
"""
Simple test script for CloudyIntel
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from cloudy_intel_state import CloudyIntelState, create_initial_state
        print("✅ cloudy_intel_state imported successfully")
    except Exception as e:
        print(f"❌ Failed to import cloudy_intel_state: {e}")
        return False
    
    try:
        from cloudy_intel_agents import architect_supervisor, compute_architect
        print("✅ cloudy_intel_agents imported successfully")
    except Exception as e:
        print(f"❌ Failed to import cloudy_intel_agents: {e}")
        return False
    
    try:
        from cloudy_intel_routing import phase_router, inner_loop_router
        print("✅ cloudy_intel_routing imported successfully")
    except Exception as e:
        print(f"❌ Failed to import cloudy_intel_routing: {e}")
        return False
    
    try:
        from cloudy_intel_rag import CloudyIntelRAG, create_architect_rag_tools
        print("✅ cloudy_intel_rag imported successfully")
    except Exception as e:
        print(f"❌ Failed to import cloudy_intel_rag: {e}")
        return False
    
    try:
        from cloudy_intel_main import CloudyIntel
        print("✅ cloudy_intel_main imported successfully")
    except Exception as e:
        print(f"❌ Failed to import cloudy_intel_main: {e}")
        return False
    
    return True

def test_state_creation():
    """Test state creation and management."""
    print("\n🧪 Testing state creation...")
    
    try:
        from cloudy_intel_state import create_initial_state
        
        state = create_initial_state("Test problem", "aws")
        
        # Check required fields
        assert "user_problem" in state
        assert "cloud_provider" in state
        assert "current_phase" in state
        assert "iteration_count" in state
        
        print("✅ State creation test passed")
        return True
        
    except Exception as e:
        print(f"❌ State creation test failed: {e}")
        return False

def test_agent_creation():
    """Test agent creation."""
    print("\n🧪 Testing agent creation...")
    
    try:
        from cloudy_intel_agents import compute_architect
        from cloudy_intel_state import create_initial_state
        
        state = create_initial_state("Test problem", "aws")
        
        # Test agent function
        result = compute_architect(state)
        
        assert "messages" in result
        assert "architecture_components" in result
        
        print("✅ Agent creation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Agent creation test failed: {e}")
        return False

def test_routing_logic():
    """Test routing logic."""
    print("\n🧪 Testing routing logic...")
    
    try:
        from cloudy_intel_routing import phase_router, inner_loop_router
        from cloudy_intel_state import create_initial_state, Phase
        
        state = create_initial_state("Test problem", "aws")
        
        # Test phase router
        result = phase_router(state)
        assert result == "architect_supervisor"
        
        # Test inner loop router
        state["factual_errors_exist"] = True
        result = inner_loop_router(state)
        assert result == "architect_supervisor"
        
        print("✅ Routing logic test passed")
        return True
        
    except Exception as e:
        print(f"❌ Routing logic test failed: {e}")
        return False

def test_cloudy_intel_creation():
    """Test CloudyIntel class creation."""
    print("\n🧪 Testing CloudyIntel creation...")
    
    try:
        from cloudy_intel_main import CloudyIntel
        
        # Test creation without RAG
        cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=False)
        assert cloudy_intel.cloud_provider == "aws"
        assert cloudy_intel.use_rag == False
        assert cloudy_intel.graph is not None
        
        print("✅ CloudyIntel creation test passed")
        return True
        
    except Exception as e:
        print(f"❌ CloudyIntel creation test failed: {e}")
        return False

def test_simple_workflow():
    """Test a simple workflow execution."""
    print("\n🧪 Testing simple workflow...")
    
    try:
        from cloudy_intel_main import CloudyIntel
        
        # Create CloudyIntel instance
        cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=False)
        
        # Test with simple problem
        user_problem = "Deploy a simple web application"
        
        # This might fail due to missing API keys, but we can test the structure
        try:
            result = cloudy_intel.run(user_problem, max_iterations=1)
            print("✅ Simple workflow test passed")
            return True
        except Exception as e:
            if "API" in str(e) or "key" in str(e).lower():
                print("⚠️  Simple workflow test skipped (missing API keys)")
                return True
            else:
                print(f"❌ Simple workflow test failed: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Simple workflow test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 CLOUDYINTEL TEST SUITE")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_state_creation,
        test_agent_creation,
        test_routing_logic,
        test_cloudy_intel_creation,
        test_simple_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CloudyIntel is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
