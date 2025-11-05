# AWS Documentation RAG Setup Guide

This guide will help you build a RAG (Retrieval Augmented Generation) system for AWS documentation.

## Overview

A RAG system allows you to:
- Store AWS documentation in a searchable vector database
- Query the documentation using natural language
- Get accurate, context-aware answers based on AWS documentation

## Prerequisites

1. Python 3.8+
2. Required Python packages (install from requirements.txt)
3. AWS documentation (either downloaded or web URLs)
4. OpenAI API key (optional, for better LLM performance)
   - Or use local models (requires more setup)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Key dependencies needed:
- langchain
- chromadb (or faiss-cpu)
- sentence-transformers (for embeddings)
- openai (optional, for OpenAI embeddings/LLM)
- unstructured (for document loading)
- requests (for downloading docs)

## Step 2: Prepare AWS Documentation

You have several options:

### Option A: Download from URLs
The script can download AWS documentation from web URLs:

```python
from aws_rag_setup import AWSDocRAGSetup, get_aws_documentation_urls

setup = AWSDocRAGSetup()
aws_urls = get_aws_documentation_urls()
setup.download_aws_docs(aws_urls)
```

### Option B: Use Local Files
Place your AWS documentation files (`.txt`, `.md`, `.pdf`) in the `data/aws_docs/` directory.

### Option C: Download AWS Documentation Manually
- Visit https://docs.aws.amazon.com/
- Download relevant documentation as PDF or markdown
- Save to `data/aws_docs/`

## Step 3: Build Vector Store

Run the setup script to:
1. Load documents
2. Chunk them into smaller pieces
3. Create embeddings
4. Store in vector database

```python
from aws_rag_setup import AWSDocRAGSetup

# Initialize setup
setup = AWSDocRAGSetup(
    docs_directory="data/aws_docs",
    vector_store_path="data/aws_vectorstore",
    chunk_size=1000,  # Adjust based on your needs
    chunk_overlap=200
)

# Load documents
documents = setup.load_documents(file_extensions=[".txt", ".md", ".pdf"])

# Chunk documents
chunks = setup.chunk_documents(documents)

# Create vector store
vectorstore = setup.create_vector_store(chunks, use_chroma=True)
```

## Step 4: Query the RAG System

Once the vector store is created, you can query it:

```python
from aws_rag_query import AWSDocRAGQuery
import os

# Initialize query system
rag_query = AWSDocRAGQuery(
    vector_store_path="data/aws_vectorstore",
    use_openai=True,  # Set to False for local models
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    k=4  # Number of documents to retrieve
)

# Ask questions
result = rag_query.query("How do I create an S3 bucket?")
print(result["answer"])

# Get formatted response with sources
response = rag_query.query_with_sources("What is AWS Lambda?")
print(response)
```

## Configuration Options

### Embeddings
- **OpenAI Embeddings**: Better quality, requires API key, costs money
- **HuggingFace Embeddings**: Free, local, good quality (default: `all-MiniLM-L6-v2`)

### Vector Store
- **ChromaDB** (recommended): Easy to use, persistent, good performance
- **FAISS**: Fast, good for large-scale, requires manual persistence

### Chunking
- **chunk_size**: Size of text chunks (default: 1000)
- **chunk_overlap**: Overlap between chunks (default: 200)
- Adjust based on your document structure and LLM context window

### Retrieval
- **k**: Number of documents to retrieve (default: 4)
- Increase for more context, decrease for faster responses

## Integration with Existing CloudyIntel System

To integrate with your existing CloudyIntel agents:

1. Add the RAG query system to your agent tools
2. Use it as a knowledge source for AWS-related questions
3. Combine with your existing agent architecture

Example integration:

```python
from aws_rag_query import AWSDocRAGQuery
from langchain.tools import Tool

# Initialize RAG
rag_query = AWSDocRAGQuery(...)

# Create a tool
aws_doc_tool = Tool(
    name="AWS Documentation",
    func=lambda q: rag_query.query(q)["answer"],
    description="Search AWS documentation for answers to questions"
)

# Add to your agent's tools
agent_tools = [aws_doc_tool, ...]
```

## Advanced Usage

### Custom Prompts
Modify the prompt template in `aws_rag_query.py` to customize the response format.

### Multiple Collections
Use different collections for different AWS services:

```python
# EC2 documentation
setup.create_vector_store(chunks, collection_name="ec2_docs")

# S3 documentation
setup.create_vector_store(chunks, collection_name="s3_docs")
```

### Hybrid Search
Combine keyword search with semantic search for better results.

### Incremental Updates
Add new documents without rebuilding the entire vector store:

```python
# Load existing vector store
vectorstore = setup.load_vector_store()

# Add new documents
new_chunks = setup.chunk_documents(new_documents)
vectorstore.add_documents(new_chunks)
```

## Troubleshooting

### Out of Memory
- Reduce chunk_size
- Use smaller embedding models
- Process documents in batches

### Poor Quality Results
- Increase k (retrieve more documents)
- Improve chunking strategy
- Use better embedding models
- Refine prompts

### Slow Performance
- Use GPU for embeddings
- Reduce k
- Use FAISS instead of ChromaDB for large datasets
- Cache embeddings

## Next Steps

1. Customize the AWS documentation URLs for your specific needs
2. Fine-tune chunking parameters based on your documents
3. Integrate with your CloudyIntel agent system
4. Add monitoring and logging
5. Implement caching for frequently asked questions

## Resources

- LangChain Documentation: https://python.langchain.com/
- ChromaDB Documentation: https://docs.trychroma.com/
- AWS Documentation: https://docs.aws.amazon.com/
- Sentence Transformers: https://www.sbert.net/
