#!/usr/bin/env python3
"""
Test script to verify the modified task decomposition logic.
This script tests that the architect supervisor properly decomposes tasks
and that domain architects reference the decomposed tasks instead of user_problem.
"""

import asyncio
from cloudy_intel_state import create_initial_state
from cloudy_intel_agents import architect_supervisor, compute_architect, network_architect
from cloudy_intel_routing import determine_relevant_agents

async def test_task_decomposition():
    """Test the task decomposition logic."""
    print("=== Testing Task Decomposition Logic ===\n")
    
    # Create initial state
    user_problem = "Deploy a scalable e-commerce backend with high availability and security"
    cloud_provider = "aws"
    
    print(f"User Problem: {user_problem}")
    print(f"Cloud Provider: {cloud_provider}")
    
    # Create initial state
    state = create_initial_state(user_problem, cloud_provider)
    print(f"Initial state created with {len(state)} fields")
    print(f"Initial decomposed_tasks: {state.get('decomposed_tasks', {})}")
    print(f"Initial task_assignments: {state.get('task_assignments', {})}")
    print()
    
    # Test architect supervisor
    print("=== Testing Architect Supervisor ===")
    state_after_supervisor = await architect_supervisor(state)
    
    print(f"Decomposed tasks after supervisor: {len(state_after_supervisor.get('decomposed_tasks', {}))}")
    print(f"Task assignments after supervisor: {len(state_after_supervisor.get('task_assignments', {}))}")
    
    # Print task assignments
    for domain, task in state_after_supervisor.get('task_assignments', {}).items():
        print(f"\n{domain.upper()} Task Assignment:")
        print(f"  {task[:100]}..." if len(task) > 100 else f"  {task}")
    
    print(f"\nActive agents: {state_after_supervisor.get('active_agents', [])}")
    print()
    
    # Test domain architect (compute)
    print("=== Testing Compute Architect ===")
    state_after_compute = await compute_architect(state_after_supervisor)
    
    compute_component = state_after_compute.get('architecture_components', {}).get('compute', {})
    print(f"Compute architect completed: {'compute_architect' in state_after_compute.get('completed_agents', [])}")
    print(f"Task assigned to compute architect: {compute_component.get('task_assigned', 'N/A')[:100]}...")
    print(f"Architecture component created: {'recommendations' in compute_component}")
    print()
    
    # Test domain architect (network)
    print("=== Testing Network Architect ===")
    state_after_network = await network_architect(state_after_supervisor)
    
    network_component = state_after_network.get('architecture_components', {}).get('network', {})
    print(f"Network architect completed: {'network_architect' in state_after_network.get('completed_agents', [])}")
    print(f"Task assigned to network architect: {network_component.get('task_assigned', 'N/A')[:100]}...")
    print(f"Architecture component created: {'recommendations' in network_component}")
    print()
    
    # Verify the logic works as expected
    print("=== Verification ===")
    
    # Check that supervisor created task assignments
    has_task_assignments = len(state_after_supervisor.get('task_assignments', {})) > 0
    print(f"✓ Supervisor created task assignments: {has_task_assignments}")
    
    # Check that domain architects used assigned tasks
    compute_used_assigned_task = 'task_assigned' in compute_component
    network_used_assigned_task = 'task_assigned' in network_component
    print(f"✓ Compute architect used assigned task: {compute_used_assigned_task}")
    print(f"✓ Network architect used assigned task: {network_used_assigned_task}")
    
    # Check that tasks are different from user problem
    compute_task = compute_component.get('task_assigned', '')
    network_task = network_component.get('task_assigned', '')
    tasks_are_specific = (compute_task != user_problem and network_task != user_problem)
    print(f"✓ Tasks are specific (not just user problem): {tasks_are_specific}")
    
    print("\n=== Test Summary ===")
    if has_task_assignments and compute_used_assigned_task and network_used_assigned_task and tasks_are_specific:
        print("✅ SUCCESS: Task decomposition logic is working correctly!")
        print("   - Architect supervisor decomposes tasks")
        print("   - Domain architects reference decomposed tasks")
        print("   - Tasks are specific and actionable")
    else:
        print("❌ FAILURE: Task decomposition logic needs fixes")
    
    return state_after_network

if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_task_decomposition())
    print(f"\nFinal state keys: {list(result.keys())}")
