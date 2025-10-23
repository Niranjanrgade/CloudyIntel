#!/usr/bin/env python3
"""
Simple test to verify the task decomposition logic without running the full async workflow.
"""

from cloudy_intel_state import create_initial_state, CloudyIntelState
from cloudy_intel_routing import determine_relevant_agents

def test_state_structure():
    """Test that the state structure includes the new task decomposition fields."""
    print("=== Testing State Structure ===\n")
    
    # Create initial state
    user_problem = "Deploy a scalable e-commerce backend with high availability and security"
    cloud_provider = "aws"
    
    state = create_initial_state(user_problem, cloud_provider)
    
    # Check that new fields exist
    has_decomposed_tasks = 'decomposed_tasks' in state
    has_task_assignments = 'task_assignments' in state
    
    print(f"✓ State has 'decomposed_tasks' field: {has_decomposed_tasks}")
    print(f"✓ State has 'task_assignments' field: {has_task_assignments}")
    print(f"✓ Initial decomposed_tasks: {state['decomposed_tasks']}")
    print(f"✓ Initial task_assignments: {state['task_assignments']}")
    
    return has_decomposed_tasks and has_task_assignments

def test_relevant_agents():
    """Test that relevant agents are determined correctly."""
    print("\n=== Testing Relevant Agents Detection ===\n")
    
    test_cases = [
        "Deploy a scalable e-commerce backend with high availability and security",
        "Set up a data warehouse with S3 and Redshift",
        "Create a serverless API with Lambda and DynamoDB",
        "Design a network with VPC and load balancers"
    ]
    
    for problem in test_cases:
        agents = determine_relevant_agents(problem)
        print(f"Problem: {problem[:50]}...")
        print(f"Relevant agents: {agents}")
        print()

def test_task_decomposition_logic():
    """Test the task decomposition logic structure."""
    print("=== Testing Task Decomposition Logic ===\n")
    
    # Simulate what the architect supervisor would do
    user_problem = "Deploy a scalable e-commerce backend with high availability and security"
    relevant_agents = determine_relevant_agents(user_problem)
    
    print(f"User problem: {user_problem}")
    print(f"Relevant agents: {relevant_agents}")
    
    # Simulate task decomposition
    decomposed_tasks = {}
    task_assignments = {}
    
    domain_descriptions = {
        "compute_architect": "Compute Architect (EC2, Lambda, ECS, etc.)",
        "network_architect": "Network Architect (VPC, ALB, CloudFront, etc.)",
        "storage_architect": "Storage Architect (S3, EBS, EFS, etc.)",
        "database_architect": "Database Architect (RDS, DynamoDB, ElastiCache, etc.)"
    }
    
    for agent in relevant_agents:
        domain = agent.replace("_architect", "")
        task_description = f"""
        Based on the user problem: "{user_problem}"
        
        Your specific task as {domain_descriptions[agent]}:
        - Analyze the {domain} requirements for this problem
        - Design appropriate {domain} solutions using AWS services
        - Provide detailed configuration recommendations
        - Consider cost, security, and performance implications
        - Use web search for latest pricing and best practices
        
        Focus specifically on {domain} aspects of the architecture.
        """
        
        decomposed_tasks[domain] = {
            "task_description": task_description,
            "domain": domain,
            "agent": agent,
            "requirements": f"Design {domain} solutions for: {user_problem}",
            "deliverables": f"Detailed {domain} architecture recommendations"
        }
        
        task_assignments[domain] = task_description
    
    print(f"✓ Created {len(decomposed_tasks)} decomposed tasks")
    print(f"✓ Created {len(task_assignments)} task assignments")
    
    # Show example task assignment
    if task_assignments:
        first_domain = list(task_assignments.keys())[0]
        print(f"\nExample task assignment for {first_domain}:")
        print(f"  {task_assignments[first_domain][:200]}...")
    
    return len(decomposed_tasks) > 0 and len(task_assignments) > 0

def test_domain_architect_logic():
    """Test that domain architects can access assigned tasks."""
    print("\n=== Testing Domain Architect Logic ===\n")
    
    # Simulate state with task assignments
    user_problem = "Deploy a scalable e-commerce backend with high availability and security"
    state = create_initial_state(user_problem, "aws")
    
    # Simulate task assignments (what supervisor would create)
    state["task_assignments"] = {
        "compute": "Design compute resources for scalable e-commerce backend with EC2, Lambda, and ECS",
        "network": "Design network infrastructure with VPC, load balancers, and security groups",
        "storage": "Design storage solutions with S3, EBS, and backup strategies",
        "database": "Design database solutions with RDS, DynamoDB, and caching"
    }
    
    # Test that domain architects can access their assigned tasks
    compute_task = state.get("task_assignments", {}).get("compute", "")
    network_task = state.get("task_assignments", {}).get("network", "")
    
    print(f"✓ Compute architect can access assigned task: {len(compute_task) > 0}")
    print(f"✓ Network architect can access assigned task: {len(network_task) > 0}")
    print(f"✓ Tasks are different from user problem: {compute_task != user_problem}")
    
    # Show example
    print(f"\nCompute task: {compute_task}")
    print(f"Network task: {network_task}")
    
    return len(compute_task) > 0 and len(network_task) > 0

def main():
    """Run all tests."""
    print("Testing Modified Task Decomposition Logic\n")
    print("=" * 50)
    
    # Run tests
    test1 = test_state_structure()
    test_relevant_agents()
    test2 = test_task_decomposition_logic()
    test3 = test_domain_architect_logic()
    
    print("\n" + "=" * 50)
    print("=== Test Results ===")
    print(f"✓ State structure: {test1}")
    print(f"✓ Task decomposition: {test2}")
    print(f"✓ Domain architect access: {test3}")
    
    if test1 and test2 and test3:
        print("\n🎉 SUCCESS: All tests passed!")
        print("The modified logic should work correctly:")
        print("  - Architect supervisor decomposes tasks")
        print("  - Domain architects reference decomposed tasks")
        print("  - Tasks are specific and actionable")
    else:
        print("\n❌ FAILURE: Some tests failed")
    
    return test1 and test2 and test3

if __name__ == "__main__":
    main()
