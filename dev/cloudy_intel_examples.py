"""
CloudyIntel Examples and Testing

This file contains example usage scenarios and testing functions for CloudyIntel.
"""

import os
import sys
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cloudy_intel_main import CloudyIntel

def example_ecommerce_backend():
    """Example: E-commerce backend architecture."""
    print("🛒 EXAMPLE: E-commerce Backend Architecture")
    print("=" * 50)
    
    user_problem = """
    Design a scalable e-commerce backend that can handle:
    - 100,000+ concurrent users
    - High availability (99.9% uptime)
    - Secure payment processing
    - Real-time inventory management
    - Global content delivery
    - Cost optimization
    """
    
    cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=True)
    result = cloudy_intel.run(user_problem, max_iterations=3)
    
    print("\n📊 RESULTS:")
    print(f"Phase: {result.get('current_phase', 'N/A')}")
    print(f"Iterations: {result.get('iteration_count', 0)}")
    print(f"Components: {len(result.get('architecture_components', {}))}")
    
    return result

def example_data_analytics_platform():
    """Example: Data analytics platform architecture."""
    print("📊 EXAMPLE: Data Analytics Platform Architecture")
    print("=" * 50)
    
    user_problem = """
    Design a data analytics platform that can:
    - Process 1TB+ of data daily
    - Support real-time and batch processing
    - Handle multiple data sources (APIs, databases, files)
    - Provide interactive dashboards
    - Ensure data security and compliance
    - Scale automatically with data growth
    """
    
    cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=True)
    result = cloudy_intel.run(user_problem, max_iterations=3)
    
    print("\n📊 RESULTS:")
    print(f"Phase: {result.get('current_phase', 'N/A')}")
    print(f"Iterations: {result.get('iteration_count', 0)}")
    print(f"Components: {len(result.get('architecture_components', {}))}")
    
    return result

def example_microservices_architecture():
    """Example: Microservices architecture."""
    print("🔧 EXAMPLE: Microservices Architecture")
    print("=" * 50)
    
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
    
    cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=True)
    result = cloudy_intel.run(user_problem, max_iterations=3)
    
    print("\n📊 RESULTS:")
    print(f"Phase: {result.get('current_phase', 'N/A')}")
    print(f"Iterations: {result.get('iteration_count', 0)}")
    print(f"Components: {len(result.get('architecture_components', {}))}")
    
    return result

def example_azure_architecture():
    """Example: Azure cloud architecture."""
    print("☁️  EXAMPLE: Azure Cloud Architecture")
    print("=" * 50)
    
    user_problem = """
    Design a hybrid cloud solution using Azure that includes:
    - On-premises integration
    - Azure Active Directory
    - Azure SQL Database
    - Azure App Service
    - Azure Functions
    - Azure Storage
    - Azure Monitor
    - Security and compliance
    """
    
    cloudy_intel = CloudyIntel(cloud_provider="azure", use_rag=True)
    result = cloudy_intel.run(user_problem, max_iterations=3)
    
    print("\n📊 RESULTS:")
    print(f"Phase: {result.get('current_phase', 'N/A')}")
    print(f"Iterations: {result.get('iteration_count', 0)}")
    print(f"Components: {len(result.get('architecture_components', {}))}")
    
    return result

def test_basic_functionality():
    """Test basic CloudyIntel functionality."""
    print("🧪 TESTING: Basic Functionality")
    print("=" * 50)
    
    # Test with simple problem
    user_problem = "Deploy a simple web application with a database"
    
    # Test without RAG
    print("\n1. Testing without RAG...")
    cloudy_intel_basic = CloudyIntel(cloud_provider="aws", use_rag=False)
    result_basic = cloudy_intel_basic.run(user_problem, max_iterations=2)
    
    print(f"✅ Basic test completed: {result_basic.get('current_phase', 'N/A')}")
    
    # Test with RAG
    print("\n2. Testing with RAG...")
    cloudy_intel_rag = CloudyIntel(cloud_provider="aws", use_rag=True)
    result_rag = cloudy_intel_rag.run(user_problem, max_iterations=2)
    
    print(f"✅ RAG test completed: {result_rag.get('current_phase', 'N/A')}")
    
    return result_basic, result_rag

def test_error_handling():
    """Test error handling scenarios."""
    print("🧪 TESTING: Error Handling")
    print("=" * 50)
    
    # Test with invalid cloud provider
    try:
        cloudy_intel = CloudyIntel(cloud_provider="invalid", use_rag=False)
        print("❌ Should have failed with invalid cloud provider")
    except Exception as e:
        print(f"✅ Correctly handled invalid cloud provider: {str(e)}")
    
    # Test with empty problem
    try:
        cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=False)
        result = cloudy_intel.run("", max_iterations=1)
        print(f"✅ Handled empty problem: {result.get('current_phase', 'N/A')}")
    except Exception as e:
        print(f"❌ Failed to handle empty problem: {str(e)}")
    
    return True

def test_iteration_limits():
    """Test iteration limit handling."""
    print("🧪 TESTING: Iteration Limits")
    print("=" * 50)
    
    # Test with very low iteration limit
    user_problem = "Design a complex multi-region architecture"
    
    cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=False)
    result = cloudy_intel.run(user_problem, max_iterations=1)
    
    print(f"✅ Iteration limit test completed: {result.get('iteration_count', 0)} iterations")
    
    return result

def run_all_examples():
    """Run all examples and tests."""
    print("🚀 RUNNING ALL CLOUDYINTEL EXAMPLES AND TESTS")
    print("=" * 60)
    
    results = {}
    
    # Run examples
    try:
        results["ecommerce"] = example_ecommerce_backend()
    except Exception as e:
        print(f"❌ E-commerce example failed: {str(e)}")
        results["ecommerce"] = {"error": str(e)}
    
    try:
        results["data_analytics"] = example_data_analytics_platform()
    except Exception as e:
        print(f"❌ Data analytics example failed: {str(e)}")
        results["data_analytics"] = {"error": str(e)}
    
    try:
        results["microservices"] = example_microservices_architecture()
    except Exception as e:
        print(f"❌ Microservices example failed: {str(e)}")
        results["microservices"] = {"error": str(e)}
    
    try:
        results["azure"] = example_azure_architecture()
    except Exception as e:
        print(f"❌ Azure example failed: {str(e)}")
        results["azure"] = {"error": str(e)}
    
    # Run tests
    try:
        results["basic_test"] = test_basic_functionality()
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        results["basic_test"] = {"error": str(e)}
    
    try:
        results["error_handling"] = test_error_handling()
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        results["error_handling"] = {"error": str(e)}
    
    try:
        results["iteration_limits"] = test_iteration_limits()
    except Exception as e:
        print(f"❌ Iteration limits test failed: {str(e)}")
        results["iteration_limits"] = {"error": str(e)}
    
    # Summary
    print("\n📊 SUMMARY OF ALL TESTS")
    print("=" * 30)
    
    for test_name, result in results.items():
        if "error" in result:
            print(f"❌ {test_name}: FAILED - {result['error']}")
        else:
            print(f"✅ {test_name}: PASSED")
    
    return results

def interactive_demo():
    """Interactive demo for CloudyIntel."""
    print("🎮 INTERACTIVE CLOUDYINTEL DEMO")
    print("=" * 40)
    
    print("Welcome to CloudyIntel! Let's design your cloud architecture.")
    print()
    
    # Get user input
    user_problem = input("Describe your cloud architecture requirements: ")
    cloud_provider = input("Choose cloud provider (aws/azure): ").lower()
    use_rag = input("Enable RAG for enhanced accuracy? (y/n): ").lower() == 'y'
    
    if cloud_provider not in ["aws", "azure"]:
        print("Invalid cloud provider. Defaulting to AWS.")
        cloud_provider = "aws"
    
    print(f"\n🚀 Starting CloudyIntel...")
    print(f"Problem: {user_problem}")
    print(f"Provider: {cloud_provider.upper()}")
    print(f"RAG: {'Enabled' if use_rag else 'Disabled'}")
    print()
    
    # Run CloudyIntel
    cloudy_intel = CloudyIntel(cloud_provider=cloud_provider, use_rag=use_rag)
    result = cloudy_intel.run(user_problem, max_iterations=5)
    
    # Show results
    summary = cloudy_intel.get_architecture_summary(result)
    print(summary)
    
    return result

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CloudyIntel Examples and Testing")
    parser.add_argument("--demo", action="store_true", help="Run interactive demo")
    parser.add_argument("--test", action="store_true", help="Run all tests")
    parser.add_argument("--example", choices=["ecommerce", "data", "microservices", "azure"], help="Run specific example")
    
    args = parser.parse_args()
    
    if args.demo:
        interactive_demo()
    elif args.test:
        run_all_examples()
    elif args.example:
        if args.example == "ecommerce":
            example_ecommerce_backend()
        elif args.example == "data":
            example_data_analytics_platform()
        elif args.example == "microservices":
            example_microservices_architecture()
        elif args.example == "azure":
            example_azure_architecture()
    else:
        print("Please specify --demo, --test, or --example")
        print("Examples:")
        print("  python cloudy_intel_examples.py --demo")
        print("  python cloudy_intel_examples.py --test")
        print("  python cloudy_intel_examples.py --example ecommerce")
