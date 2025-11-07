"""
AWS Documentation RAG Setup Script
This script sets up a RAG (Retrieval Augmented Generation) system for AWS documentation.
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    WebBaseLoader,
    DirectoryLoader,
    UnstructuredMarkdownLoader
)
from langchain.schema import Document
import chromadb
from chromadb.config import Settings


class AWSDocRAGSetup:
    """Class to handle AWS documentation RAG setup"""
    
    def __init__(
        self,
        docs_directory: str = "data/aws_docs",
        vector_store_path: str = "data/aws_vectorstore",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        use_openai: bool = False,
        openai_api_key: Optional[str] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize AWS RAG Setup
        
        Args:
            docs_directory: Directory to store AWS documentation
            vector_store_path: Path to store vector embeddings
            embedding_model: HuggingFace model name for embeddings
            use_openai: Whether to use OpenAI embeddings (requires API key)
            openai_api_key: OpenAI API key if using OpenAI embeddings
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.docs_directory = Path(docs_directory)
        self.vector_store_path = Path(vector_store_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Create directories
        self.docs_directory.mkdir(parents=True, exist_ok=True)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings
        if use_openai:
            if not openai_api_key:
                raise ValueError("OpenAI API key required when use_openai=True")
            os.environ["OPENAI_API_KEY"] = openai_api_key
            self.embeddings = OpenAIEmbeddings()
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=embedding_model,
                model_kwargs={'device': 'cpu'}  # Use 'cuda' if GPU available
            )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def download_aws_docs(self, urls: List[str], save_format: str = "markdown"):
        """
        Download AWS documentation from URLs
        
        Args:
            urls: List of AWS documentation URLs
            save_format: Format to save documents (markdown, html, text)
        """
        print(f"Downloading AWS documentation from {len(urls)} URLs...")
        
        for idx, url in enumerate(urls):
            try:
                print(f"Downloading {idx+1}/{len(urls)}: {url}")
                loader = WebBaseLoader(url)
                documents = loader.load()
                
                # Save document
                filename = url.split("/")[-1] or f"doc_{idx}"
                filepath = self.docs_directory / f"{filename}.{save_format}"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    for doc in documents:
                        f.write(doc.page_content)
                
                print(f"Saved to {filepath}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")
        
        print("Download complete!")
    
    def load_documents(self, file_extensions: List[str] = [".txt", ".md", ".pdf"]) -> List[Document]:
        """
        Load documents from the docs directory
        
        Args:
            file_extensions: List of file extensions to load
            
        Returns:
            List of Document objects
        """
        documents = []
        
        for ext in file_extensions:
            loader = DirectoryLoader(
                str(self.docs_directory),
                glob=f"**/*{ext}",
                loader_cls={
                    ".txt": TextLoader,
                    ".md": UnstructuredMarkdownLoader,
                    ".pdf": PyPDFLoader
                }.get(ext, TextLoader)
            )
            docs = loader.load()
            documents.extend(docs)
        
        print(f"Loaded {len(documents)} documents")
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        print(f"Chunking {len(documents)} documents...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(
        self,
        documents: List[Document],
        use_chroma: bool = True,
        collection_name: str = "aws_docs"
    ):
        """
        Create vector store from documents
        
        Args:
            documents: List of Document objects (should be chunked)
            use_chroma: Whether to use ChromaDB (True) or FAISS (False)
            collection_name: Name of ChromaDB collection
        """
        print(f"Creating vector store from {len(documents)} documents...")
        
        if use_chroma:
            # Create ChromaDB vector store
            vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=str(self.vector_store_path),
                collection_name=collection_name
            )
            print(f"ChromaDB vector store created at {self.vector_store_path}")
        else:
            # Create FAISS vector store
            vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            vectorstore.save_local(str(self.vector_store_path))
            print(f"FAISS vector store saved at {self.vector_store_path}")
        
        return vectorstore
    
    def load_vector_store(self, use_chroma: bool = True, collection_name: str = "aws_docs"):
        """
        Load existing vector store
        
        Args:
            use_chroma: Whether using ChromaDB (True) or FAISS (False)
            collection_name: Name of ChromaDB collection
            
        Returns:
            Vector store object
        """
        if use_chroma:
            vectorstore = Chroma(
                persist_directory=str(self.vector_store_path),
                embedding_function=self.embeddings,
                collection_name=collection_name
            )
        else:
            vectorstore = FAISS.load_local(
                str(self.vector_store_path),
                self.embeddings
            )
        
        print(f"Vector store loaded from {self.vector_store_path}")
        return vectorstore


def get_aws_documentation_urls() -> List[str]:
    """
    Get list of important AWS documentation URLs
    
    Returns:
        List of AWS documentation URLs
    """
    # Common AWS documentation URLs - customize based on your needs
    urls = [
        "https://docs.aws.amazon.com/",
        "https://docs.aws.amazon.com/ec2/",
        "https://docs.aws.amazon.com/s3/",
        "https://docs.aws.amazon.com/lambda/",
        "https://docs.aws.amazon.com/rds/",
        "https://docs.aws.amazon.com/iam/",
        "https://docs.aws.amazon.com/vpc/",
        "https://docs.aws.amazon.com/cloudformation/",
        # Add more specific documentation pages as needed
    ]
    return urls


if __name__ == "__main__":
    # Example usage
    setup = AWSDocRAGSetup(
        docs_directory="data/aws_docs",
        vector_store_path="data/aws_vectorstore",
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Option 1: Download documentation (uncomment if needed)
    # aws_urls = get_aws_documentation_urls()
    # setup.download_aws_docs(aws_urls)
    
    # Option 2: Load existing documents
    documents = setup.load_documents(file_extensions=[".txt", ".md", ".pdf"])
    
    # Chunk documents
    chunks = setup.chunk_documents(documents)
    
    # Create vector store
    vectorstore = setup.create_vector_store(chunks, use_chroma=True)
    
    print("RAG setup complete!")

