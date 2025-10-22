from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from cloudy_intel_state import CloudyIntelState, Phase, mark_agent_complete

# Initialize LLM and tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
serper = GoogleSerperAPIWrapper()

# Tools
tool_web_search = Tool(
    name="web_search",
    func=serper.run,
    description="Useful for when you need more information from an online search"
)

tools = [tool_web_search]
llm_with_tools = llm.bind_tools(tools)

# =============================================================================
# PHASE 1: ARCHITECT TEAM
# =============================================================================

def architect_supervisor(state: CloudyIntelState) -> CloudyIntelState:
    """Supervisor that coordinates all architect agents."""
    system_prompt = f"""
    You are the Architect Supervisor for {state['cloud_provider'].upper()} cloud architecture.
    Your role is to decompose the user problem and coordinate domain architects.
    
    User Problem: {state['user_problem']}
    Current Iteration: {state['iteration_count']}
    
    Available feedback:
    - Validation Feedback: {state['validation_feedback']}
    - Audit Feedback: {state['audit_feedback']}
    
    Decompose the problem into tasks for:
    1. Compute Architect (EC2, Lambda, ECS, etc.)
    2. Network Architect (VPC, ALB, CloudFront, etc.)
    3. Storage Architect (S3, EBS, EFS, etc.)
    4. Database Architect (RDS, DynamoDB, ElastiCache, etc.)
    
    Provide clear instructions for each domain architect.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = state.copy()
    new_state["messages"].append(response)
    new_state["active_agents"] = ["compute_architect", "network_architect", "storage_architect", "database_architect"]
    new_state["completed_agents"] = []
    
    return new_state

def compute_architect(state: CloudyIntelState) -> CloudyIntelState:
    """AWS/Azure compute domain architect."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Compute Domain Architect.
    Design compute resources for: {state['user_problem']}
    
    Consider:
    - EC2 instances (types, sizing, placement)
    - Lambda functions (serverless compute)
    - ECS/EKS (container orchestration)
    - Auto Scaling Groups
    - Load Balancers
    
    Use web search for latest pricing and instance types.
    Provide detailed configuration recommendations.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm_with_tools.invoke(messages)
    
    new_state = mark_agent_complete(state, "compute_architect")
    new_state["messages"].append(response)
    new_state["architecture_components"]["compute"] = {
        "recommendations": response.content,
        "agent": "compute_architect"
    }
    
    return new_state

def network_architect(state: CloudyIntelState) -> CloudyIntelState:
    """AWS/Azure network domain architect."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Network Domain Architect.
    Design network infrastructure for: {state['user_problem']}
    
    Consider:
    - VPC design and subnets
    - Security Groups and NACLs
    - Load Balancers (ALB, NLB, CLB)
    - CloudFront/CDN
    - Route 53 DNS
    - VPN/Direct Connect
    
    Use web search for latest networking best practices.
    Provide detailed network architecture.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm_with_tools.invoke(messages)
    
    new_state = mark_agent_complete(state, "network_architect")
    new_state["messages"].append(response)
    new_state["architecture_components"]["network"] = {
        "recommendations": response.content,
        "agent": "network_architect"
    }
    
    return new_state

def storage_architect(state: CloudyIntelState) -> CloudyIntelState:
    """AWS/Azure storage domain architect."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Storage Domain Architect.
    Design storage solutions for: {state['user_problem']}
    
    Consider:
    - S3 buckets (object storage)
    - EBS volumes (block storage)
    - EFS (file storage)
    - Storage classes and lifecycle policies
    - Backup and disaster recovery
    
    Use web search for latest storage options and pricing.
    Provide detailed storage architecture.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm_with_tools.invoke(messages)
    
    new_state = mark_agent_complete(state, "storage_architect")
    new_state["messages"].append(response)
    new_state["architecture_components"]["storage"] = {
        "recommendations": response.content,
        "agent": "storage_architect"
    }
    
    return new_state

def database_architect(state: CloudyIntelState) -> CloudyIntelState:
    """AWS/Azure database domain architect."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Database Domain Architect.
    Design database solutions for: {state['user_problem']}
    
    Consider:
    - RDS (managed relational databases)
    - DynamoDB (NoSQL)
    - ElastiCache (caching)
    - Redshift (data warehouse)
    - Database security and encryption
    
    Use web search for latest database services and pricing.
    Provide detailed database architecture.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm_with_tools.invoke(messages)
    
    new_state = mark_agent_complete(state, "database_architect")
    new_state["messages"].append(response)
    new_state["architecture_components"]["database"] = {
        "recommendations": response.content,
        "agent": "database_architect"
    }
    
    return new_state

# =============================================================================
# PHASE 2: VALIDATOR TEAM
# =============================================================================

def validator_supervisor(state: CloudyIntelState) -> CloudyIntelState:
    """Supervisor that coordinates all validator agents."""
    system_prompt = f"""
    You are the Validator Supervisor for {state['cloud_provider'].upper()} architecture validation.
    Your role is to coordinate domain validators to check factual correctness.
    
    Architecture to validate: {state['architecture_components']}
    
    Coordinate validation for:
    1. Compute Validator (check EC2, Lambda, ECS configurations)
    2. Network Validator (check VPC, security groups, routing)
    3. Storage Validator (check S3, EBS, EFS configurations)
    4. Database Validator (check RDS, DynamoDB, ElastiCache)
    
    Focus on technical correctness and compatibility.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = state.copy()
    new_state["messages"].append(response)
    new_state["active_agents"] = ["compute_validator", "network_validator", "storage_validator", "database_validator"]
    new_state["completed_agents"] = []
    new_state["current_phase"] = Phase.VALIDATE
    
    return new_state

def compute_validator(state: CloudyIntelState) -> CloudyIntelState:
    """Validate compute architecture for technical correctness."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Compute Validator.
    Validate the compute architecture for technical correctness.
    
    Architecture to validate: {state['architecture_components'].get('compute', {})}
    
    Check for:
    - Instance type compatibility
    - Region availability
    - Pricing accuracy
    - Service limits
    - Best practices
    
    Report any factual errors or optimization opportunities.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "compute_validator")
    new_state["messages"].append(response)
    
    # Extract validation feedback
    validation_feedback = {
        "domain": "compute",
        "agent": "compute_validator",
        "feedback": response.content,
        "has_errors": "error" in response.content.lower()
    }
    
    if "validation_feedback" not in new_state:
        new_state["validation_feedback"] = []
    new_state["validation_feedback"].append(validation_feedback)
    
    return new_state

def network_validator(state: CloudyIntelState) -> CloudyIntelState:
    """Validate network architecture for technical correctness."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Network Validator.
    Validate the network architecture for technical correctness.
    
    Architecture to validate: {state['architecture_components'].get('network', {})}
    
    Check for:
    - Subnet configurations
    - Security group rules
    - Routing table setup
    - Load balancer configurations
    - DNS settings
    
    Report any factual errors or optimization opportunities.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "network_validator")
    new_state["messages"].append(response)
    
    validation_feedback = {
        "domain": "network",
        "agent": "network_validator",
        "feedback": response.content,
        "has_errors": "error" in response.content.lower()
    }
    
    if "validation_feedback" not in new_state:
        new_state["validation_feedback"] = []
    new_state["validation_feedback"].append(validation_feedback)
    
    return new_state

def storage_validator(state: CloudyIntelState) -> CloudyIntelState:
    """Validate storage architecture for technical correctness."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Storage Validator.
    Validate the storage architecture for technical correctness.
    
    Architecture to validate: {state['architecture_components'].get('storage', {})}
    
    Check for:
    - Storage class configurations
    - Lifecycle policies
    - Encryption settings
    - Access permissions
    - Backup configurations
    
    Report any factual errors or optimization opportunities.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "storage_validator")
    new_state["messages"].append(response)
    
    validation_feedback = {
        "domain": "storage",
        "agent": "storage_validator",
        "feedback": response.content,
        "has_errors": "error" in response.content.lower()
    }
    
    if "validation_feedback" not in new_state:
        new_state["validation_feedback"] = []
    new_state["validation_feedback"].append(validation_feedback)
    
    return new_state

def database_validator(state: CloudyIntelState) -> CloudyIntelState:
    """Validate database architecture for technical correctness."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Database Validator.
    Validate the database architecture for technical correctness.
    
    Architecture to validate: {state['architecture_components'].get('database', {})}
    
    Check for:
    - Database engine compatibility
    - Instance sizing
    - Backup configurations
    - Security settings
    - Performance optimization
    
    Report any factual errors or optimization opportunities.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "database_validator")
    new_state["messages"].append(response)
    
    validation_feedback = {
        "domain": "database",
        "agent": "database_validator",
        "feedback": response.content,
        "has_errors": "error" in response.content.lower()
    }
    
    if "validation_feedback" not in new_state:
        new_state["validation_feedback"] = []
    new_state["validation_feedback"].append(validation_feedback)
    
    return new_state

# =============================================================================
# PHASE 3: PILLAR AUDITOR TEAM
# =============================================================================

def pillar_audit_supervisor(state: CloudyIntelState) -> CloudyIntelState:
    """Supervisor that coordinates all pillar auditors."""
    system_prompt = f"""
    You are the Pillar Audit Supervisor for {state['cloud_provider'].upper()} architecture auditing.
    Your role is to coordinate pillar auditors to check design quality.
    
    Architecture to audit: {state['architecture_components']}
    
    Coordinate auditing for:
    1. Security Auditor (security best practices)
    2. Cost Auditor (cost optimization)
    3. Reliability Auditor (reliability and availability)
    4. Performance Auditor (performance optimization)
    5. Operational Excellence Auditor (operational best practices)
    
    Focus on design quality and best practice violations.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = state.copy()
    new_state["messages"].append(response)
    new_state["active_agents"] = ["security_auditor", "cost_auditor", "reliability_auditor", "performance_auditor", "operational_excellence_auditor"]
    new_state["completed_agents"] = []
    new_state["current_phase"] = Phase.AUDIT
    
    return new_state

def security_auditor(state: CloudyIntelState) -> CloudyIntelState:
    """Audit architecture for security best practices."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Security Auditor.
    Audit the architecture for security best practices.
    
    Architecture to audit: {state['architecture_components']}
    
    Check for:
    - Network security (VPC, security groups, NACLs)
    - Data encryption (at rest and in transit)
    - Access controls (IAM, RBAC)
    - Compliance requirements
    - Security monitoring and logging
    
    Report any security flaws or recommendations.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "security_auditor")
    new_state["messages"].append(response)
    
    audit_feedback = {
        "pillar": "security",
        "agent": "security_auditor",
        "feedback": response.content,
        "has_flaws": "flaw" in response.content.lower() or "issue" in response.content.lower()
    }
    
    if "audit_feedback" not in new_state:
        new_state["audit_feedback"] = []
    new_state["audit_feedback"].append(audit_feedback)
    
    return new_state

def cost_auditor(state: CloudyIntelState) -> CloudyIntelState:
    """Audit architecture for cost optimization."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Cost Auditor.
    Audit the architecture for cost optimization opportunities.
    
    Architecture to audit: {state['architecture_components']}
    
    Check for:
    - Right-sizing recommendations
    - Reserved instance opportunities
    - Spot instance usage
    - Storage optimization
    - Unused resources
    
    Report any cost optimization opportunities.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "cost_auditor")
    new_state["messages"].append(response)
    
    audit_feedback = {
        "pillar": "cost",
        "agent": "cost_auditor",
        "feedback": response.content,
        "has_flaws": "optimization" in response.content.lower() or "cost" in response.content.lower()
    }
    
    if "audit_feedback" not in new_state:
        new_state["audit_feedback"] = []
    new_state["audit_feedback"].append(audit_feedback)
    
    return new_state

def reliability_auditor(state: CloudyIntelState) -> CloudyIntelState:
    """Audit architecture for reliability and availability."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Reliability Auditor.
    Audit the architecture for reliability and availability.
    
    Architecture to audit: {state['architecture_components']}
    
    Check for:
    - Multi-AZ deployments
    - Auto Scaling configurations
    - Load balancing
    - Backup and disaster recovery
    - Monitoring and alerting
    
    Report any reliability issues or recommendations.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "reliability_auditor")
    new_state["messages"].append(response)
    
    audit_feedback = {
        "pillar": "reliability",
        "agent": "reliability_auditor",
        "feedback": response.content,
        "has_flaws": "issue" in response.content.lower() or "improvement" in response.content.lower()
    }
    
    if "audit_feedback" not in new_state:
        new_state["audit_feedback"] = []
    new_state["audit_feedback"].append(audit_feedback)
    
    return new_state

def performance_auditor(state: CloudyIntelState) -> CloudyIntelState:
    """Audit architecture for performance optimization."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Performance Auditor.
    Audit the architecture for performance optimization.
    
    Architecture to audit: {state['architecture_components']}
    
    Check for:
    - CDN configurations
    - Caching strategies
    - Database optimization
    - Network performance
    - Resource allocation
    
    Report any performance optimization opportunities.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "performance_auditor")
    new_state["messages"].append(response)
    
    audit_feedback = {
        "pillar": "performance",
        "agent": "performance_auditor",
        "feedback": response.content,
        "has_flaws": "optimization" in response.content.lower() or "improvement" in response.content.lower()
    }
    
    if "audit_feedback" not in new_state:
        new_state["audit_feedback"] = []
    new_state["audit_feedback"].append(audit_feedback)
    
    return new_state

def operational_excellence_auditor(state: CloudyIntelState) -> CloudyIntelState:
    """Audit architecture for operational excellence."""
    system_prompt = f"""
    You are a {state['cloud_provider'].upper()} Operational Excellence Auditor.
    Audit the architecture for operational best practices.
    
    Architecture to audit: {state['architecture_components']}
    
    Check for:
    - Monitoring and logging
    - Automation opportunities
    - Deployment strategies
    - Change management
    - Documentation and runbooks
    
    Report any operational improvement opportunities.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = mark_agent_complete(state, "operational_excellence_auditor")
    new_state["messages"].append(response)
    
    audit_feedback = {
        "pillar": "operational_excellence",
        "agent": "operational_excellence_auditor",
        "feedback": response.content,
        "has_flaws": "improvement" in response.content.lower() or "enhancement" in response.content.lower()
    }
    
    if "audit_feedback" not in new_state:
        new_state["audit_feedback"] = []
    new_state["audit_feedback"].append(audit_feedback)
    
    return new_state

# =============================================================================
# FINAL PRESENTER
# =============================================================================

def final_presenter(state: CloudyIntelState) -> CloudyIntelState:
    """Present the final approved architecture."""
    system_prompt = f"""
    You are the Final Presenter for CloudyIntel.
    Present the final approved architecture.
    
    User Problem: {state['user_problem']}
    Final Architecture: {state['architecture_components']}
    Cloud Provider: {state['cloud_provider'].upper()}
    
    Create a comprehensive presentation including:
    1. Executive Summary
    2. Architecture Overview
    3. Component Details
    4. Cost Estimation
    5. Security Considerations
    6. Implementation Plan
    
    Make it professional and actionable.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    response = llm.invoke(messages)
    
    new_state = state.copy()
    new_state["messages"].append(response)
    new_state["current_phase"] = Phase.COMPLETE
    new_state["final_architecture"] = state["architecture_components"]
    new_state["architecture_summary"] = response.content
    
    return new_state
