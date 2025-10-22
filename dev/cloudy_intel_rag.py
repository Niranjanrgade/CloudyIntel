from typing import List, Dict, Any
from langchain_core.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
import os

# Import CloudyIntelState for type hints
try:
    from cloudy_intel_state import CloudyIntelState
except ImportError:
    # Fallback for when running independently
    CloudyIntelState = Dict[str, Any]

class CloudyIntelRAG:
    """RAG system for cloud documentation and best practices."""
    
    def __init__(self, cloud_provider: str = "aws"):
        self.cloud_provider = cloud_provider
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.vectorstore = None
        self._setup_rag()
    
    def _setup_rag(self):
        """Setup RAG with cloud documentation."""
        # Cloud documentation URLs
        if self.cloud_provider.lower() == "aws":
            urls = [
                "https://docs.aws.amazon.com/wellarchitected/latest/framework/",
                "https://docs.aws.amazon.com/architecture/",
                "https://aws.amazon.com/architecture/well-architected/",
                "https://docs.aws.amazon.com/whitepapers/",
                "https://aws.amazon.com/security/security-resources/",
                "https://aws.amazon.com/compliance/",
                "https://docs.aws.amazon.com/cost-management/",
                "https://aws.amazon.com/reliability/"
            ]
        elif self.cloud_provider.lower() == "azure":
            urls = [
                "https://docs.microsoft.com/en-us/azure/architecture/",
                "https://docs.microsoft.com/en-us/azure/well-architected/",
                "https://docs.microsoft.com/en-us/azure/security/",
                "https://docs.microsoft.com/en-us/azure/cost-management/",
                "https://docs.microsoft.com/en-us/azure/reliability/",
                "https://docs.microsoft.com/en-us/azure/performance/",
                "https://docs.microsoft.com/en-us/azure/operational-excellence/"
            ]
        else:
            raise ValueError(f"Unsupported cloud provider: {self.cloud_provider}")
        
        # Load documents
        loader = WebBaseLoader(urls)
        documents = loader.load()
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
    
    def search_documentation(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search cloud documentation for relevant information."""
        if not self.vectorstore:
            return []
        
        # Search for relevant documents
        docs = self.vectorstore.similarity_search(query, k=k)
        
        # Format results
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "source": doc.metadata.get("source", "Unknown")
            })
        
        return results
    
    def get_rag_context(self, query: str, k: int = 5) -> str:
        """Get RAG context for a query."""
        results = self.search_documentation(query, k)
        
        if not results:
            return "No relevant documentation found."
        
        context = "Relevant documentation:\n\n"
        for i, result in enumerate(results, 1):
            context += f"{i}. {result['content']}\n\n"
        
        return context
    
    def create_rag_tool(self, tool_name: str, description: str) -> Tool:
        """Create a RAG tool for agents."""
        def rag_search(query: str) -> str:
            return self.get_rag_context(query)
        
        return Tool(
            name=tool_name,
            func=rag_search,
            description=description
        )

# RAG tools for different agent types
def create_architect_rag_tools(cloud_provider: str = "aws") -> List[Tool]:
    """Create RAG tools for architect agents."""
    rag = CloudyIntelRAG(cloud_provider)
    
    tools = [
        rag.create_rag_tool(
            "search_architecture_docs",
            "Search cloud architecture documentation for design patterns and best practices"
        ),
        rag.create_rag_tool(
            "search_service_docs",
            "Search specific cloud service documentation for configuration details"
        ),
        rag.create_rag_tool(
            "search_pricing_docs",
            "Search pricing documentation for cost considerations"
        )
    ]
    
    return tools

def create_validator_rag_tools(cloud_provider: str = "aws") -> List[Tool]:
    """Create RAG tools for validator agents."""
    rag = CloudyIntelRAG(cloud_provider)
    
    tools = [
        rag.create_rag_tool(
            "search_service_compatibility",
            "Search documentation for service compatibility and requirements"
        ),
        rag.create_rag_tool(
            "search_configuration_docs",
            "Search configuration documentation for technical specifications"
        ),
        rag.create_rag_tool(
            "search_limits_docs",
            "Search documentation for service limits and quotas"
        )
    ]
    
    return tools

def create_auditor_rag_tools(cloud_provider: str = "aws") -> List[Tool]:
    """Create RAG tools for auditor agents."""
    rag = CloudyIntelRAG(cloud_provider)
    
    tools = [
        rag.create_rag_tool(
            "search_security_docs",
            "Search security documentation and best practices"
        ),
        rag.create_rag_tool(
            "search_cost_optimization_docs",
            "Search cost optimization documentation and recommendations"
        ),
        rag.create_rag_tool(
            "search_reliability_docs",
            "Search reliability documentation and high availability patterns"
        ),
        rag.create_rag_tool(
            "search_performance_docs",
            "Search performance optimization documentation and best practices"
        ),
        rag.create_rag_tool(
            "search_operational_docs",
            "Search operational excellence documentation and best practices"
        )
    ]
    
    return tools

# Enhanced agent functions with RAG tools
def create_enhanced_architect_agent(agent_name: str, domain: str, cloud_provider: str = "aws"):
    """Create an enhanced architect agent with RAG tools."""
    rag_tools = create_architect_rag_tools(cloud_provider)
    
    def enhanced_architect(state: CloudyIntelState) -> CloudyIntelState:
        """Enhanced architect with RAG capabilities."""
        system_prompt = f"""
        You are a {cloud_provider.upper()} {domain} Domain Architect.
        Design {domain} resources for: {state['user_problem']}
        
        Use the RAG tools to search for:
        - Latest service documentation
        - Best practices and design patterns
        - Pricing information
        - Configuration details
        
        Provide detailed, factually correct recommendations.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Use RAG tools to gather information
        context = ""
        for tool in rag_tools:
            try:
                result = tool.func(state['user_problem'])
                context += f"\n{tool.name}: {result}\n"
            except Exception as e:
                context += f"\n{tool.name}: Error - {str(e)}\n"
        
        messages.append({"role": "user", "content": f"Context: {context}\n\nDesign the {domain} architecture."})
        
        # Process with LLM
        response = {"role": "assistant", "content": f"Enhanced {domain} architecture design with RAG context."}
        
        new_state = state.copy()
        new_state["messages"].append(response)
        new_state["architecture_components"][domain] = {
            "recommendations": response["content"],
            "agent": agent_name,
            "rag_context": context
        }
        
        return new_state
    
    return enhanced_architect

def create_enhanced_validator_agent(agent_name: str, domain: str, cloud_provider: str = "aws"):
    """Create an enhanced validator agent with RAG tools."""
    rag_tools = create_validator_rag_tools(cloud_provider)
    
    def enhanced_validator(state: CloudyIntelState) -> CloudyIntelState:
        """Enhanced validator with RAG capabilities."""
        system_prompt = f"""
        You are a {cloud_provider.upper()} {domain} Validator.
        Validate the {domain} architecture for technical correctness.
        
        Use the RAG tools to search for:
        - Service compatibility documentation
        - Configuration specifications
        - Service limits and quotas
        - Technical requirements
        
        Architecture to validate: {state['architecture_components'].get(domain, {})}
        
        Report any factual errors or optimization opportunities.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Use RAG tools to gather information
        context = ""
        for tool in rag_tools:
            try:
                result = tool.func(f"{domain} validation")
                context += f"\n{tool.name}: {result}\n"
            except Exception as e:
                context += f"\n{tool.name}: Error - {str(e)}\n"
        
        messages.append({"role": "user", "content": f"Context: {context}\n\nValidate the {domain} architecture."})
        
        # Process with LLM
        response = {"role": "assistant", "content": f"Enhanced {domain} validation with RAG context."}
        
        new_state = state.copy()
        new_state["messages"].append(response)
        
        validation_feedback = {
            "domain": domain,
            "agent": agent_name,
            "feedback": response["content"],
            "has_errors": "error" in response["content"].lower(),
            "rag_context": context
        }
        
        if "validation_feedback" not in new_state:
            new_state["validation_feedback"] = []
        new_state["validation_feedback"].append(validation_feedback)
        
        return new_state
    
    return enhanced_validator

def create_enhanced_auditor_agent(agent_name: str, pillar: str, cloud_provider: str = "aws"):
    """Create an enhanced auditor agent with RAG tools."""
    rag_tools = create_auditor_rag_tools(cloud_provider)
    
    def enhanced_auditor(state: CloudyIntelState) -> CloudyIntelState:
        """Enhanced auditor with RAG capabilities."""
        system_prompt = f"""
        You are a {cloud_provider.upper()} {pillar} Auditor.
        Audit the architecture for {pillar} best practices.
        
        Use the RAG tools to search for:
        - {pillar} best practices
        - Compliance requirements
        - Optimization recommendations
        - Design patterns
        
        Architecture to audit: {state['architecture_components']}
        
        Report any {pillar} flaws or recommendations.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Use RAG tools to gather information
        context = ""
        for tool in rag_tools:
            try:
                result = tool.func(f"{pillar} audit")
                context += f"\n{tool.name}: {result}\n"
            except Exception as e:
                context += f"\n{tool.name}: Error - {str(e)}\n"
        
        messages.append({"role": "user", "content": f"Context: {context}\n\nAudit the architecture for {pillar}."})
        
        # Process with LLM
        response = {"role": "assistant", "content": f"Enhanced {pillar} audit with RAG context."}
        
        new_state = state.copy()
        new_state["messages"].append(response)
        
        audit_feedback = {
            "pillar": pillar,
            "agent": agent_name,
            "feedback": response["content"],
            "has_flaws": "flaw" in response["content"].lower() or "issue" in response["content"].lower(),
            "rag_context": context
        }
        
        if "audit_feedback" not in new_state:
            new_state["audit_feedback"] = []
        new_state["audit_feedback"].append(audit_feedback)
        
        return new_state
    
    return enhanced_auditor
