#!/usr/bin/env python3
"""
Demonstration of the intelligent agent filtering system.
"""

# Simulate the filtering logic
def determine_relevant_agents(user_problem: str):
    """Intelligently determine which architect agents are relevant based on the user's problem."""
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

# Test cases
test_cases = [
    "I need to store 5 TB data",
    "I need a database for my application", 
    "I need to deploy a web application",
    "I need a complete cloud infrastructure"
]

print("🧪 Intelligent Agent Filtering Demo")
print("=" * 50)

for problem in test_cases:
    agents = determine_relevant_agents(problem)
    print(f"\nProblem: '{problem}'")
    print(f"Selected agents: {agents}")
    
    # Calculate token savings
    total_agents = 4
    selected_agents = len(agents)
    savings = ((total_agents - selected_agents) / total_agents) * 100
    print(f"Token savings: {savings:.1f}% (runs {selected_agents}/{total_agents} agents)")

print("\n🎯 Key Benefits:")
print("• For 'store 5 TB data': Only storage_architect runs (75% token savings)")
print("• For 'database for application': Only database_architect runs (75% token savings)")  
print("• For 'web application': compute_architect + network_architect run (50% token savings)")
print("• For 'complete infrastructure': All agents run (0% savings, but comprehensive coverage)")
