"""
AWS Documentation RAG Query Script
This script queries the AWS documentation RAG system to answer questions.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI, HuggingFacePipeline
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document


class AWSDocRAGQuery:
    """Class to handle querying AWS documentation RAG system"""
    
    def __init__(
        self,
        vector_store_path: str = "data/aws_vectorstore",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        use_openai: bool = False,
        openai_api_key: Optional[str] = None,
        use_chroma: bool = True,
        collection_name: str = "aws_docs",
        llm_model: str = "gpt-3.5-turbo",
        temperature: float = 0.0,
        k: int = 4  # Number of documents to retrieve
    ):
        """
        Initialize AWS RAG Query system
        
        Args:
            vector_store_path: Path to vector store
            embedding_model: HuggingFace model name for embeddings
            use_openai: Whether to use OpenAI embeddings/LLM
            openai_api_key: OpenAI API key
            use_chroma: Whether using ChromaDB (True) or FAISS (False)
            collection_name: ChromaDB collection name
            llm_model: LLM model name
            temperature: Temperature for LLM
            k: Number of documents to retrieve
        """
        self.vector_store_path = Path(vector_store_path)
        self.k = k
        
        # Initialize embeddings
        if use_openai:
            if not openai_api_key:
                raise ValueError("OpenAI API key required when use_openai=True")
            os.environ["OPENAI_API_KEY"] = openai_api_key
            self.embeddings = OpenAIEmbeddings()
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=embedding_model,
                model_kwargs={'device': 'cpu'}
            )
        
        # Load vector store
        if use_chroma:
            self.vectorstore = Chroma(
                persist_directory=str(self.vector_store_path),
                embedding_function=self.embeddings,
                collection_name=collection_name
            )
        else:
            self.vectorstore = FAISS.load_local(
                str(self.vector_store_path),
                self.embeddings
            )
        
        # Initialize LLM
        if use_openai:
            self.llm = ChatOpenAI(
                model_name=llm_model,
                temperature=temperature
            )
        else:
            # For local models, you can use HuggingFacePipeline
            # This requires additional setup
            raise NotImplementedError("Local LLM setup not implemented. Use OpenAI for now.")
        
        # Create retrieval chain
        self.setup_retrieval_chain()
    
    def setup_retrieval_chain(self):
        """Setup the retrieval QA chain"""
        # Custom prompt template
        prompt_template = """Use the following pieces of AWS documentation context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer: Provide a detailed, accurate answer based on the AWS documentation context. If the context doesn't contain enough information, say so.
"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": self.k}
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
    
    def query(self, question: str) -> Dict:
        """
        Query the RAG system
        
        Args:
            question: Question to ask about AWS documentation
            
        Returns:
            Dictionary with answer and source documents
        """
        result = self.qa_chain({"query": question})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"]
        }
    
    def retrieve_documents(self, query: str, k: Optional[int] = None) -> List[Document]:
        """
        Retrieve relevant documents without generating answer
        
        Args:
            query: Query string
            k: Number of documents to retrieve (uses self.k if None)
            
        Returns:
            List of relevant documents
        """
        k = k or self.k
        docs = self.vectorstore.similarity_search(query, k=k)
        return docs
    
    def query_with_sources(self, question: str) -> str:
        """
        Query and return formatted answer with sources
        
        Args:
            question: Question to ask
            
        Returns:
            Formatted string with answer and sources
        """
        result = self.query(question)
        
        response = f"Question: {question}\n\n"
        response += f"Answer: {result['answer']}\n\n"
        response += "Sources:\n"
        
        for i, doc in enumerate(result['source_documents'], 1):
            source = doc.metadata.get('source', 'Unknown')
            response += f"{i}. {source}\n"
        
        return response


def main():
    """Example usage"""
    # Initialize RAG query system
    # Make sure to set your OpenAI API key if using OpenAI
    rag_query = AWSDocRAGQuery(
        vector_store_path="data/aws_vectorstore",
        use_openai=True,  # Set to False if using local models
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        k=4
    )
    
    # Example queries
    questions = [
        "How do I create an S3 bucket?",
        "What is AWS Lambda?",
        "How do I set up VPC peering?",
        "What are the best practices for EC2 security?"
    ]
    
    for question in questions:
        print("\n" + "="*80)
        response = rag_query.query_with_sources(question)
        print(response)
        print("="*80)


if __name__ == "__main__":
    main()
