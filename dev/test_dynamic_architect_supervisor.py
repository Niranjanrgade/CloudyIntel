"""
Test script to demonstrate the new dynamic architect_supervisor functionality.
This shows how the supervisor now uses LLM to decompose tasks instead of hardcoded assignments.
"""

import asyncio
from cloudy_intel_state import create_initial_state
from cloudy_intel_agents import architect_supervisor

async def test_dynamic_architect_supervisor():
    """Test the dynamic architect supervisor with different problem types."""
    
    # Test Case 1: E-commerce website problem
    print("=" * 60)
    print("TEST CASE 1: E-commerce Website Architecture")
    print("=" * 60)
    
    ecommerce_problem = """
    I need to build a scalable e-commerce website that can handle:
    - 100,000 concurrent users during peak shopping seasons
    - Product catalog with 1M+ products and images
    - Real-time inventory management
    - Secure payment processing
    - Global content delivery
    - Mobile-first responsive design
    """
    
    state1 = create_initial_state(ecommerce_problem, "aws")
    result1 = await architect_supervisor(state1)
    
    print(f"User Problem: {result1['user_problem'][:100]}...")
    print(f"Relevant Agents: {result1['active_agents']}")
    print(f"Supervisor Analysis: {result1['supervisor_analysis'][:200]}...")
    print(f"Task Assignments: {list(result1['task_assignments'].keys())}")
    
    # Test Case 2: Data Analytics problem
    print("\n" + "=" * 60)
    print("TEST CASE 2: Data Analytics Platform")
    print("=" * 60)
    
    analytics_problem = """
    I need to build a data analytics platform for:
    - Processing 10TB of IoT sensor data daily
    - Real-time stream processing
    - Machine learning model training and inference
    - Data lake storage with different access patterns
    - Interactive dashboards for business users
    """
    
    state2 = create_initial_state(analytics_problem, "aws")
    result2 = await architect_supervisor(state2)
    
    print(f"User Problem: {result2['user_problem'][:100]}...")
    print(f"Relevant Agents: {result2['active_agents']}")
    print(f"Supervisor Analysis: {result2['supervisor_analysis'][:200]}...")
    print(f"Task Assignments: {list(result2['task_assignments'].keys())}")
    
    # Test Case 3: Simple web app (should trigger fewer agents)
    print("\n" + "=" * 60)
    print("TEST CASE 3: Simple Web Application")
    print("=" * 60)
    
    simple_problem = """
    I need a simple web application for a small business:
    - Basic company website with contact forms
    - Blog functionality
    - Low traffic (under 1000 visitors/month)
    - Cost-effective solution
    """
    
    state3 = create_initial_state(simple_problem, "aws")
    result3 = await architect_supervisor(state3)
    
    print(f"User Problem: {result3['user_problem'][:100]}...")
    print(f"Relevant Agents: {result3['active_agents']}")
    print(f"Supervisor Analysis: {result3['supervisor_analysis'][:200]}...")
    print(f"Task Assignments: {list(result3['task_assignments'].keys())}")
    
    # Test Case 4: Iteration with feedback
    print("\n" + "=" * 60)
    print("TEST CASE 4: Iteration with Previous Feedback")
    print("=" * 60)
    
    # Simulate a second iteration with feedback
    state4 = create_initial_state(ecommerce_problem, "aws")
    state4["iteration_count"] = 1
    state4["validation_feedback"] = [
        {
            "domain": "compute",
            "agent": "compute_validator", 
            "feedback": "EC2 instance types need to be updated for better performance",
            "has_errors": True
        }
    ]
    state4["audit_feedback"] = [
        {
            "pillar": "security",
            "agent": "security_auditor",
            "feedback": "Missing encryption at rest for database",
            "has_flaws": True
        }
    ]
    
    result4 = await architect_supervisor(state4)
    
    print(f"User Problem: {result4['user_problem'][:100]}...")
    print(f"Iteration: {result4['iteration_count']}")
    print(f"Previous Feedback Available: {len(result4.get('validation_feedback', []))} validation, {len(result4.get('audit_feedback', []))} audit")
    print(f"Supervisor Analysis: {result4['supervisor_analysis'][:200]}...")

if __name__ == "__main__":
    asyncio.run(test_dynamic_architect_supervisor())
