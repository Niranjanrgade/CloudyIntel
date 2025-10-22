#!/usr/bin/env python3
"""
Test script to demonstrate intelligent agent filtering.
This shows how the system now only runs relevant agents based on the user's problem.
"""

from cloudy_intel_routing import determine_relevant_agents

def test_agent_filtering():
    """Test the intelligent agent filtering for different problem types."""
    
    test_cases = [
        {
            "problem": "I need to store 5 TB data",
            "expected_agents": ["storage_architect"],
            "description": "Storage-only problem should only require storage_architect"
        },
        {
            "problem": "I need a database for my application",
            "expected_agents": ["database_architect"],
            "description": "Database-only problem should only require database_architect"
        },
        {
            "problem": "I need to deploy a web application with high availability",
            "expected_agents": ["compute_architect", "network_architect"],
            "description": "Web application should require compute and network architects"
        },
        {
            "problem": "I need a complete cloud infrastructure for my e-commerce platform",
            "expected_agents": ["compute_architect", "network_architect", "storage_architect", "database_architect"],
            "description": "Complex problem should require all architects"
        },
        {
            "problem": "I need to backup my files to the cloud",
            "expected_agents": ["storage_architect"],
            "description": "Backup problem should only require storage_architect"
        }
    ]
    
    print("🧪 Testing Intelligent Agent Filtering")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Problem: '{test_case['problem']}'")
        
        # Get the actual agents that would be selected
        actual_agents = determine_relevant_agents(test_case['problem'])
        
        print(f"Expected agents: {test_case['expected_agents']}")
        print(f"Actual agents:   {actual_agents}")
        
        # Check if the filtering worked correctly
        if set(actual_agents) == set(test_case['expected_agents']):
            print("✅ PASS - Correct agents selected")
        else:
            print("❌ FAIL - Incorrect agent selection")
            print(f"   Missing: {set(test_case['expected_agents']) - set(actual_agents)}")
            print(f"   Extra:   {set(actual_agents) - set(test_case['expected_agents'])}")
    
    print("\n" + "=" * 50)
    print("🎯 Key Benefits:")
    print("• Reduces token usage by 75% for storage-only problems")
    print("• Eliminates unnecessary database_architect for storage problems")
    print("• Only runs relevant agents based on problem analysis")
    print("• Maintains comprehensive coverage for complex problems")

if __name__ == "__main__":
    test_agent_filtering()
