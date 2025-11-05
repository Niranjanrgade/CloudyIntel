"""
Example: Complete AWS RAG Workflow
This script demonstrates the end-to-end process of setting up and using AWS documentation RAG.
"""

import os
from aws_rag_setup import AWSDocRAGSetup, get_aws_documentation_urls
from aws_rag_query import AWSDocRAGQuery


def setup_rag_system():
    """Step 1: Setup the RAG system by processing documents"""
    print("="*80)
    print("STEP 1: Setting up RAG System")
    print("="*80)
    
    # Initialize setup
    setup = AWSDocRAGSetup(
        docs_directory="data/aws_docs",
        vector_store_path="data/aws_vectorstore",
        chunk_size=1000,
        chunk_overlap=200,
        use_openai=False  # Set to True if you have OpenAI API key
    )
    
    # Option A: Download documentation from URLs (uncomment if needed)
    # print("\nDownloading AWS documentation...")
    # aws_urls = get_aws_documentation_urls()
    # setup.download_aws_docs(aws_urls)
    
    # Option B: Load existing documents
    print("\nLoading documents from data/aws_docs/...")
    documents = setup.load_documents(file_extensions=[".txt", ".md", ".pdf"])
    
    if len(documents) == 0:
        print("\n⚠️  WARNING: No documents found in data/aws_docs/")
        print("Please add AWS documentation files (.txt, .md, or .pdf) to the directory first.")
        print("\nYou can:")
        print("1. Download docs manually and save to data/aws_docs/")
        print("2. Uncomment the download section above to fetch from URLs")
        return None
    
    # Chunk documents
    print("\nChunking documents...")
    chunks = setup.chunk_documents(documents)
    
    # Create vector store
    print("\nCreating vector store...")
    vectorstore = setup.create_vector_store(chunks, use_chroma=True)
    
    print("\n✅ RAG setup complete!")
    return vectorstore


def query_rag_system():
    """Step 2: Query the RAG system"""
    print("\n" + "="*80)
    print("STEP 2: Querying RAG System")
    print("="*80)
    
    # Check if vector store exists
    if not os.path.exists("data/aws_vectorstore"):
        print("\n❌ ERROR: Vector store not found!")
        print("Please run setup_rag_system() first.")
        return
    
    # Initialize query system
    # Note: For production, use environment variables for API keys
    use_openai = os.getenv("OPENAI_API_KEY") is not None
    
    if use_openai:
        print("\nUsing OpenAI for embeddings and LLM...")
    else:
        print("\nUsing HuggingFace embeddings (local, free)...")
        print("⚠️  Note: For LLM, you'll need OpenAI API key or local LLM setup")
    
    try:
        rag_query = AWSDocRAGQuery(
            vector_store_path="data/aws_vectorstore",
            use_openai=use_openai,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            k=4
        )
        
        # Example queries
        questions = [
            "What is AWS Lambda?",
            "How do I create an S3 bucket?",
            "What are EC2 instance types?",
            "How do I configure VPC security groups?"
        ]
        
        print("\n" + "-"*80)
        print("Example Queries")
        print("-"*80)
        
        for i, question in enumerate(questions, 1):
            print(f"\n📝 Query {i}: {question}")
            print("-"*80)
            
            try:
                # Retrieve relevant documents
                docs = rag_query.retrieve_documents(question, k=3)
                print(f"\nFound {len(docs)} relevant documents:")
                for j, doc in enumerate(docs, 1):
                    source = doc.metadata.get('source', 'Unknown')
                    print(f"  {j}. {source}")
                    print(f"     Preview: {doc.page_content[:100]}...")
                
                # Query with answer generation (requires LLM)
                if use_openai:
                    result = rag_query.query(question)
                    print(f"\n💡 Answer: {result['answer']}")
                else:
                    print("\n⚠️  Skipping answer generation (requires OpenAI API key or local LLM)")
                    
            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
            
            print("-"*80)
            
    except Exception as e:
        print(f"\n❌ Error initializing query system: {e}")
        print("\nPossible solutions:")
        print("1. Make sure the vector store exists (run setup first)")
        print("2. Install required dependencies: pip install -r requirements.txt")
        print("3. Set OPENAI_API_KEY environment variable if using OpenAI")


def main():
    """Main function to run the complete workflow"""
    print("\n" + "="*80)
    print("AWS Documentation RAG - Complete Workflow Example")
    print("="*80)
    
    # Step 1: Setup (comment out if already done)
    print("\n🔧 Step 1: Setup RAG System")
    vectorstore = setup_rag_system()
    
    if vectorstore is None:
        print("\n⚠️  Setup incomplete. Please add documents and try again.")
        return
    
    # Step 2: Query
    print("\n🔍 Step 2: Query RAG System")
    query_rag_system()
    
    print("\n" + "="*80)
    print("Workflow Complete!")
    print("="*80)
    print("\nNext steps:")
    print("1. Customize the AWS documentation sources")
    print("2. Adjust chunking parameters for better results")
    print("3. Integrate with your CloudyIntel agent system")
    print("4. Set OPENAI_API_KEY for better answer quality")


if __name__ == "__main__":
    main()
