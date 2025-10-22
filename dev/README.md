# CloudyIntel - Multi-Agent Cloud Architecture Design System

## 🚀 Overview

CloudyIntel is a sophisticated, agentic AI system that autonomously generates, validates, and audits cloud infrastructure designs for AWS and Azure. It implements a "three-phase, dual-loop" cyclical workflow that mimics real-world engineering review processes.

## 🏗️ Architecture

### Three-Phase Workflow

1. **Phase 1: Generation (Architect Team)**
   - Supervisor: Architect_Supervisor
   - Agents: Compute_Architect, Network_Architect, Storage_Architect, Database_Architect
   - Tools: Web Search + RAG (Cloud Documentation)

2. **Phase 2: Validation (Validator Team)**
   - Supervisor: Validator_Supervisor
   - Agents: Compute_Validator, Network_Validator, Storage_Validator, Database_Validator
   - Tools: RAG-Only (Cloud Documentation)

3. **Phase 3: Audit (Pillar Auditor Team)**
   - Supervisor: Pillar_Audit_Supervisor
   - Agents: Security_Auditor, Cost_Auditor, Reliability_Auditor, Performance_Auditor, Operational_Excellence_Auditor
   - Tools: RAG-Only (Well-Architected Framework)

### Cyclical Workflow

- **Inner Loop**: Returns to Phase 1 if factual errors exist
- **Outer Loop**: Returns to Phase 1 if design flaws exist
- **Completion**: Proceeds to final presentation when all quality gates pass

## 📁 File Structure

```
dev/
├── cloudy_intel_state.py          # State management and data structures
├── cloudy_intel_agents.py         # Agent implementations (supervisors and specialists)
├── cloudy_intel_routing.py        # Conditional routing logic
├── cloudy_intel_rag.py            # RAG tools for cloud documentation
├── cloudy_intel_graph.py          # Graph compilation and execution
├── cloudy_intel_main.py           # Main execution and orchestration
├── cloudy_intel_examples.py      # Examples and testing
└── README.md                      # This file
```

## 🛠️ Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   # Create .env file
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key
   ```

3. **Install Additional Dependencies for RAG**
   ```bash
   pip install faiss-cpu  # For vector storage
   pip install langchain-community  # For document loaders
   ```

## 🚀 Quick Start

### Basic Usage

```python
from cloudy_intel_main import CloudyIntel

# Create CloudyIntel instance
cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=True)

# Run the workflow
result = cloudy_intel.run(
    user_problem="Deploy a scalable e-commerce backend",
    max_iterations=5
)

# Get architecture summary
summary = cloudy_intel.get_architecture_summary(result)
print(summary)
```

### Interactive Demo

```bash
python cloudy_intel_examples.py --demo
```

### Run Examples

```bash
# Run all examples and tests
python cloudy_intel_examples.py --test

# Run specific example
python cloudy_intel_examples.py --example ecommerce
```

## 🔧 Configuration

### Cloud Providers

- **AWS**: Full support with AWS Well-Architected Framework
- **Azure**: Full support with Azure Well-Architected Framework

### RAG Enhancement

- **Enabled**: Agents use RAG tools for enhanced accuracy
- **Disabled**: Agents use basic web search only

### Iteration Limits

- **Default**: 5 iterations maximum
- **Customizable**: Set via `max_iterations` parameter

## 📊 State Management

The system uses a comprehensive state model that tracks:

- **Workflow State**: Current phase, iteration count, active agents
- **Architecture**: Proposed components, validation feedback, audit feedback
- **Quality Gates**: Factual errors, design flaws, completion status
- **Metadata**: Cloud provider, session ID, timestamps

## 🔄 Workflow Details

### Phase 1: Generation
1. Architect_Supervisor decomposes the user problem
2. Domain architects work in parallel to design components
3. All architects must complete before proceeding

### Phase 2: Validation
1. Validator_Supervisor coordinates validation tasks
2. Domain validators check technical correctness
3. Inner loop: Return to Phase 1 if factual errors exist

### Phase 3: Audit
1. Pillar_Audit_Supervisor coordinates audit tasks
2. Pillar auditors check design quality and best practices
3. Outer loop: Return to Phase 1 if design flaws exist

### Completion
1. Final_Presenter creates comprehensive architecture summary
2. All quality gates must pass for completion

## 🧪 Testing

### Basic Functionality Test
```python
from cloudy_intel_examples import test_basic_functionality
test_basic_functionality()
```

### Error Handling Test
```python
from cloudy_intel_examples import test_error_handling
test_error_handling()
```

### Iteration Limits Test
```python
from cloudy_intel_examples import test_iteration_limits
test_iteration_limits()
```

## 📈 Examples

### E-commerce Backend
```python
user_problem = """
Design a scalable e-commerce backend that can handle:
- 100,000+ concurrent users
- High availability (99.9% uptime)
- Secure payment processing
- Real-time inventory management
- Global content delivery
- Cost optimization
"""
```

### Data Analytics Platform
```python
user_problem = """
Design a data analytics platform that can:
- Process 1TB+ of data daily
- Support real-time and batch processing
- Handle multiple data sources
- Provide interactive dashboards
- Ensure data security and compliance
- Scale automatically with data growth
"""
```

### Microservices Architecture
```python
user_problem = """
Design a microservices architecture for a SaaS application with:
- User management service
- Payment processing service
- Notification service
- Analytics service
- API gateway
- Service discovery
- Monitoring and logging
- CI/CD pipeline
"""
```

## 🔍 RAG Tools

### Architect RAG Tools
- `search_architecture_docs`: Design patterns and best practices
- `search_service_docs`: Service configuration details
- `search_pricing_docs`: Cost considerations

### Validator RAG Tools
- `search_service_compatibility`: Service compatibility and requirements
- `search_configuration_docs`: Technical specifications
- `search_limits_docs`: Service limits and quotas

### Auditor RAG Tools
- `search_security_docs`: Security best practices
- `search_cost_optimization_docs`: Cost optimization recommendations
- `search_reliability_docs`: High availability patterns
- `search_performance_docs`: Performance optimization
- `search_operational_docs`: Operational excellence

## 🚨 Error Handling

- **Invalid Cloud Provider**: Defaults to AWS
- **Empty User Problem**: Handles gracefully
- **Iteration Limits**: Prevents infinite loops
- **RAG Failures**: Falls back to basic web search
- **Agent Failures**: Continues with available agents

## 📝 Output Format

The system provides:

1. **Architecture Components**: Detailed recommendations for each domain
2. **Validation Feedback**: Technical correctness issues
3. **Audit Feedback**: Design quality and best practice violations
4. **Final Summary**: Comprehensive architecture presentation
5. **Metadata**: Session information and iteration tracking

## 🔧 Customization

### Adding New Agents
1. Implement agent function in `cloudy_intel_agents.py`
2. Add node to graph in `cloudy_intel_main.py`
3. Update routing logic in `cloudy_intel_routing.py`

### Adding New RAG Tools
1. Implement RAG tool in `cloudy_intel_rag.py`
2. Add to agent tool list
3. Update agent functions to use new tools

### Modifying Workflow
1. Update state model in `cloudy_intel_state.py`
2. Modify routing logic in `cloudy_intel_routing.py`
3. Update graph structure in `cloudy_intel_main.py`

## 📚 Dependencies

- **LangGraph**: Graph-based workflow orchestration
- **LangChain**: LLM integration and tool management
- **OpenAI**: GPT models for agent reasoning
- **FAISS**: Vector storage for RAG
- **Google Serper**: Web search capabilities
- **Python-dotenv**: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions, issues, or contributions:

1. Check the examples in `cloudy_intel_examples.py`
2. Review the test cases for usage patterns
3. Open an issue for bugs or feature requests
4. Submit a pull request for contributions

---

**CloudyIntel** - Transforming cloud architecture design through intelligent multi-agent collaboration! 🚀☁️
