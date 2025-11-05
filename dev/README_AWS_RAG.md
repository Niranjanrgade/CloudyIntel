# AWS Documentation RAG - Quick Start

A complete RAG (Retrieval Augmented Generation) system for querying AWS documentation.

## Quick Start (3 Steps)

### 1. Install Dependencies

```bash
pip install -r dev/requirements_rag.txt
```

### 2. Add AWS Documentation

Place your AWS documentation files in `data/aws_docs/`:
- `.txt` files
- `.md` files  
- `.pdf` files

Or use the script to download from URLs (see guide).

### 3. Run the Example

```bash
cd dev
python example_aws_rag.py
```

## Files Overview

- **`aws_rag_setup.py`**: Setup script to process documents and create vector store
- **`aws_rag_query.py`**: Query script to ask questions about AWS documentation
- **`example_aws_rag.py`**: Complete workflow example
- **`aws_rag_guide.md`**: Comprehensive setup and usage guide

## Basic Usage

```python
from aws_rag_setup import AWSDocRAGSetup
from aws_rag_query import AWSDocRAGQuery

# Setup (run once)
setup = AWSDocRAGSetup()
documents = setup.load_documents()
chunks = setup.chunk_documents(documents)
setup.create_vector_store(chunks)

# Query (use anytime)
rag = AWSDocRAGQuery(use_openai=True, openai_api_key="your-key")
result = rag.query("How do I create an S3 bucket?")
print(result["answer"])
```

## Configuration

- **Free**: Use HuggingFace embeddings (default, no API key needed)
- **Better Quality**: Use OpenAI embeddings + LLM (requires API key)

Set environment variable:
```bash
export OPENAI_API_KEY="your-key-here"
```

## Next Steps

See `aws_rag_guide.md` for:
- Detailed setup instructions
- Configuration options
- Integration with CloudyIntel agents
- Advanced usage patterns
