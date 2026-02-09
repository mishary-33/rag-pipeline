"""
Document Processor Module
Handles loading and chunking documents for the RAG pipeline
"""

import warnings
warnings.filterwarnings('ignore')

import os
from typing import List, Dict, Any
from pathlib import Path

# Document loaders - UPDATED IMPORTS
from langchain_community.document_loaders import (
    Docx2txtLoader,
    TextLoader
)

from langchain_core.documents import Document

# Text splitter - UPDATED IMPORT
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import config


class DocumentProcessor:
    """Process documents for RAG pipeline"""
    
    def __init__(self):
        """Initialize document processor with chunking strategy"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.supported_extensions = config.SUPPORTED_FILE_TYPES
    
    def load_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Load a single document and return its content with metadata"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        if file_extension not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        print(f"📄 Loading: {file_path.name}")
        
        try:
            if file_extension == ".pdf":
                # Use pdfplumber for better Arabic support
                import pdfplumber
                
                documents = []
                with pdfplumber.open(str(file_path)) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            doc = Document(
                                page_content=text,
                                metadata={"page": page_num + 1, "source": str(file_path)}
                            )
                            documents.append(doc)
            
            elif file_extension == ".docx":
                loader = Docx2txtLoader(str(file_path))
                documents = loader.load()
            
            elif file_extension == ".txt":
                loader = TextLoader(str(file_path), encoding='utf-8')
                documents = loader.load()
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add filename to metadata
            for chunk in chunks:
                chunk.metadata['source_file'] = file_path.name
            
            print(f"   ✅ {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            raise Exception(f"Error loading {file_path.name}: {str(e)}")
    
    def load_documents(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Load multiple documents
        
        Args:
            file_paths: List of paths to document files
            
        Returns:
            Combined list of all document chunks with metadata
        """
        all_chunks = []
        
        print(f"\n📚 Loading {len(file_paths)} document(s)...")
        print("=" * 60)
        
        for file_path in file_paths:
            try:
                chunks = self.load_document(file_path)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"   ❌ Failed to load {file_path}: {str(e)}")
                continue
        
        print("=" * 60)
        print(f"✅ Total chunks loaded: {len(all_chunks)}")
        
        return all_chunks
    
    def get_document_stats(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about processed documents
        
        Args:
            chunks: List of document chunks
            
        Returns:
            Dictionary with statistics
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_characters": 0,
                "unique_sources": 0,
                "sources": []
            }
        
        # Get unique sources
        sources = list(set([chunk.metadata.get('source_file', 'unknown') for chunk in chunks]))
        
        # Calculate total characters
        total_chars = sum(len(chunk.page_content) for chunk in chunks)
        
        stats = {
            "total_chunks": len(chunks),
            "total_characters": total_chars,
            "unique_sources": len(sources),
            "sources": sources,
            "avg_chunk_size": total_chars // len(chunks) if chunks else 0
        }
        
        return stats
    
    def preview_chunks(self, chunks: List[Dict[str, Any]], num_chunks: int = 3):
        """
        Preview first few chunks for inspection
        
        Args:
            chunks: List of document chunks
            num_chunks: Number of chunks to preview
        """
        print(f"\n🔍 Preview of first {num_chunks} chunk(s):")
        print("=" * 60)
        
        for i, chunk in enumerate(chunks[:num_chunks]):
            print(f"\n📄 Chunk {i+1}:")
            print(f"   Source: {chunk.metadata.get('source_file', 'unknown')}")
            print(f"   Page: {chunk.metadata.get('page', 'N/A')}")
            print(f"   Length: {len(chunk.page_content)} characters")
            print(f"\n   Content Preview:")
            print(f"   {chunk.page_content[:200]}...")
            print("-" * 60)


# Convenience function for quick testing
def process_documents(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Quick function to process documents
    
    Args:
        file_paths: List of document file paths
        
    Returns:
        List of processed chunks
    """
    processor = DocumentProcessor()
    chunks = processor.load_documents(file_paths)
    return chunks