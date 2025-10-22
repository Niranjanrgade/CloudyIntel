"""
Async Example for CloudyIntel

This example demonstrates how to use the async CloudyIntel system
with concurrent agent execution for improved performance.
"""

import asyncio
import time
from cloudy_intel_main import CloudyIntel

async def run_async_example():
    """Example of running CloudyIntel with async/await."""
    print("🚀 CloudyIntel Async Example")
    print("=" * 50)
    
    # Create CloudyIntel instance
    cloudy_intel = CloudyIntel(cloud_provider="aws", use_rag=True)
    
    # Example problem
    user_problem = """
    Design a scalable microservices architecture for a fintech application that needs to:
    - Handle 1M+ transactions per day
    - Ensure PCI DSS compliance
    - Support real-time fraud detection
    - Provide 99.99% uptime
    - Scale globally across multiple regions
    """
    
    print(f"📋 Problem: {user_problem.strip()}")
    print("\n⏱️  Starting async execution...")
    
    start_time = time.time()
    
    try:
        # Run the async workflow
        result = await cloudy_intel.run(user_problem, max_iterations=3)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n⏱️  Execution Time: {execution_time:.2f} seconds")
        
        # Get architecture summary
        summary = cloudy_intel.get_architecture_summary(result)
        print("\n" + "=" * 60)
        print("📊 ARCHITECTURE SUMMARY")
        print("=" * 60)
        print(summary)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"error": str(e)}

async def run_parallel_examples():
    """Example of running multiple CloudyIntel instances in parallel."""
    print("🚀 CloudyIntel Parallel Execution Example")
    print("=" * 50)
    
    # Different problems for parallel execution
    problems = [
        "Design a data analytics platform for processing 10TB of data daily",
        "Create a serverless web application with global CDN and auto-scaling",
        "Build a machine learning pipeline for real-time image processing"
    ]
    
    # Create multiple CloudyIntel instances
    cloudy_intel_instances = [
        CloudyIntel(cloud_provider="aws", use_rag=True),
        CloudyIntel(cloud_provider="aws", use_rag=True),
        CloudyIntel(cloud_provider="aws", use_rag=True)
    ]
    
    print(f"🔄 Running {len(problems)} parallel CloudyIntel instances...")
    start_time = time.time()
    
    try:
        # Run all instances in parallel
        tasks = [
            instance.run(problem, max_iterations=2)
            for instance, problem in zip(cloudy_intel_instances, problems)
        ]
        
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n⏱️  Total Parallel Execution Time: {execution_time:.2f} seconds")
        print(f"📊 Average Time per Instance: {execution_time/len(problems):.2f} seconds")
        
        # Print results summary
        for i, result in enumerate(results):
            print(f"\n📋 Problem {i+1} Results:")
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Completed in phase: {result.get('current_phase', 'N/A')}")
                print(f"🏗️  Components: {len(result.get('architecture_components', {}))}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error in parallel execution: {str(e)}")
        return [{"error": str(e)}] * len(problems)

async def main():
    """Main async function."""
    print("🌟 CloudyIntel Async Examples")
    print("=" * 60)
    
    # Example 1: Single async execution
    print("\n1️⃣ Single Async Execution")
    print("-" * 30)
    await run_async_example()
    
    # Example 2: Parallel execution
    print("\n\n2️⃣ Parallel Execution")
    print("-" * 30)
    await run_parallel_examples()
    
    print("\n🎉 All examples completed!")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
