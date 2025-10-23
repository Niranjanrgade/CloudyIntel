"""
Comparison between old hardcoded architect_supervisor and new dynamic architect_supervisor.
This demonstrates the improvements in task decomposition.
"""

from typing import Dict, Any, List
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def old_hardcoded_architect_supervisor(user_problem: str, cloud_provider: str = "aws") -> Dict[str, Any]:
    """
    OLD APPROACH: Hardcoded task assignments
    This is what the original architect_supervisor looked like with hardcoded tasks.
    """
    # Hardcoded domain tasks - same for every problem
    architecture_domain_tasks = {
        "compute": {
            "task_description": "Design compute infrastructure including EC2 instances, Lambda functions, ECS/EKS containers, and Auto Scaling Groups",
            "key_requirements": "Performance, scalability, cost optimization",
            "aws_services": ["EC2", "Lambda", "ECS", "EKS", "Auto Scaling Groups", "Load Balancers"],
            "deliverables": "Compute architecture recommendations with specific instance types and configurations"
        },
        "network": {
            "task_description": "Design network infrastructure including VPC, subnets, security groups, load balancers, and DNS",
            "key_requirements": "Security, high availability, performance",
            "aws_services": ["VPC", "Subnets", "Security Groups", "ALB", "NLB", "CloudFront", "Route 53"],
            "deliverables": "Network architecture with security groups, routing, and DNS configuration"
        },
        "storage": {
            "task_description": "Design storage solutions including object storage, block storage, and file systems",
            "key_requirements": "Durability, availability, performance, cost",
            "aws_services": ["S3", "EBS", "EFS", "FSx", "Storage Gateway"],
            "deliverables": "Storage architecture with backup and disaster recovery strategies"
        },
        "database": {
            "task_description": "Design database solutions including relational and NoSQL databases with caching",
            "key_requirements": "Performance, availability, consistency, backup",
            "aws_services": ["RDS", "DynamoDB", "ElastiCache", "Redshift", "DocumentDB"],
            "deliverables": "Database architecture with replication and backup strategies"
        }
    }
    
    return {
        "architecture_domain_tasks": architecture_domain_tasks,
        "active_agents": ["compute_architect", "network_architect", "storage_architect", "database_architect"],
        "completed_agents": [],
        "approach": "HARDCODED - Same tasks for every problem"
    }

async def new_dynamic_architect_supervisor(user_problem: str, cloud_provider: str = "aws", iteration_count: int = 0, previous_feedback: List = None) -> Dict[str, Any]:
    """
    NEW APPROACH: Dynamic task decomposition using LLM
    This is the improved architect_supervisor that analyzes the problem and creates specific tasks.
    """
    
    # Build context from previous iterations if available
    previous_context = ""
    if iteration_count > 0 and previous_feedback:
        previous_context = f"""
        Previous iteration feedback:
        - Validation Feedback: {previous_feedback}
        """
    
    system_prompt = f"""
    You are the Architect Supervisor for {cloud_provider.upper()} cloud architecture.
    Your role is to intelligently decompose the user problem into specific, actionable tasks for domain architects.
    
    USER PROBLEM: {user_problem}
    CURRENT ITERATION: {iteration_count}
    CLOUD PROVIDER: {cloud_provider.upper()}
    
    {previous_context}
    
    Based on the problem analysis, you need to decompose this problem into specific tasks for the following domain architects:
    - Compute Architect (EC2, Lambda, ECS, EKS, Auto Scaling, etc.)
    - Network Architect (VPC, Subnets, Security Groups, Load Balancers, DNS, etc.)
    - Storage Architect (S3, EBS, EFS, FSx, Storage Gateway, etc.)
    - Database Architect (RDS, DynamoDB, ElastiCache, Redshift, etc.)
    
    For each domain architect, you must provide:
    1. A specific, actionable task description tailored to the user's problem
    2. Key requirements and constraints specific to this problem
    3. Expected deliverables that address the user's needs
    4. Any dependencies or considerations between domains
    5. Specific {cloud_provider.upper()} services to focus on
    
    IMPORTANT: Make each task specific to the user's actual problem, not generic. Consider:
    - The specific use case and requirements
    - The scale and complexity of the problem
    - Any constraints mentioned in the problem
    - The relationships between different architectural domains
    
    Format your response as a structured breakdown where each domain architect gets a clear, focused, and problem-specific task.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = await llm.ainvoke(messages)
    
    # Parse the LLM response to extract specific tasks for each domain
    decomposed_tasks = {}
    task_assignments = {}
    
    # Create specific task assignments for each domain based on LLM analysis
    domains = ["compute", "network", "storage", "database"]
    domain_descriptions = {
        "compute": "Compute Architect (EC2, Lambda, ECS, EKS, Auto Scaling, etc.)",
        "network": "Network Architect (VPC, Subnets, Security Groups, Load Balancers, DNS, etc.)",
        "storage": "Storage Architect (S3, EBS, EFS, FSx, Storage Gateway, etc.)",
        "database": "Database Architect (RDS, DynamoDB, ElastiCache, Redshift, etc.)"
    }
    
    for domain in domains:
        # Create a more specific task based on the supervisor's analysis
        task_description = f"""
        ARCHITECT SUPERVISOR ANALYSIS:
        {response.content}
        
        YOUR SPECIFIC TASK as {domain_descriptions[domain]}:
        Based on the user problem: "{user_problem}"
        
        Analyze the {domain} requirements for this specific problem and design appropriate {domain} solutions using {cloud_provider.upper()} services.
        
        Focus on:
        - Requirements specific to this use case
        - {cloud_provider.upper()} services most relevant to the problem
        - Detailed configuration recommendations
        - Cost, security, and performance implications
        - Integration with other architectural components
        
        Provide actionable recommendations that directly address the user's problem.
        """
        
        decomposed_tasks[domain] = {
            "task_description": task_description,
            "domain": domain,
            "agent": f"{domain}_architect",
            "requirements": f"Design {domain} solutions for: {user_problem}",
            "deliverables": f"Detailed {domain} architecture recommendations",
            "supervisor_analysis": response.content,
            "cloud_provider": cloud_provider.upper()
        }
        
        task_assignments[domain] = task_description
    
    return {
        "decomposed_tasks": decomposed_tasks,
        "task_assignments": task_assignments,
        "supervisor_analysis": response.content,
        "active_agents": [f"{domain}_architect" for domain in domains],
        "completed_agents": [],
        "approach": "DYNAMIC - LLM analyzes problem and creates specific tasks"
    }

async def compare_approaches():
    """Compare old hardcoded vs new dynamic approaches."""
    
    test_problems = [
        {
            "name": "E-commerce Platform",
            "problem": "Build a scalable e-commerce website for 100K concurrent users with global CDN, secure payments, and real-time inventory"
        },
        {
            "name": "Data Analytics Platform", 
            "problem": "Create a data analytics platform for processing 10TB daily IoT data with ML training and real-time dashboards"
        },
        {
            "name": "Simple Blog",
            "problem": "Host a simple company blog with contact forms for under 1000 visitors/month"
        }
    ]
    
    for test_case in test_problems:
        print("=" * 80)
        print(f"TEST CASE: {test_case['name']}")
        print("=" * 80)
        print(f"Problem: {test_case['problem']}")
        print()
        
        # Old approach
        print("OLD HARDCODED APPROACH:")
        old_result = old_hardcoded_architect_supervisor(test_case['problem'])
        print(f"Approach: {old_result['approach']}")
        print("Task for Compute Architect:")
        print(f"  {old_result['architecture_domain_tasks']['compute']['task_description']}")
        print()
        
        # New approach
        print("NEW DYNAMIC APPROACH:")
        new_result = await new_dynamic_architect_supervisor(test_case['problem'])
        print(f"Approach: {new_result['approach']}")
        print("Supervisor Analysis:")
        print(f"  {new_result['supervisor_analysis'][:300]}...")
        print()
        print("Task for Compute Architect:")
        print(f"  {new_result['task_assignments']['compute'][:300]}...")
        print()
        print("-" * 80)
        print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(compare_approaches())
