"""
Document Processor Module
Loads and chunks documents for the RAG pipeline
"""

import warnings
warnings.filterwarnings('ignore')

from typing import List
from pathlib import Path

# Updated LangChain imports
from langchain_community.document_loaders import Docx2txtLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import config


class DocumentProcessor:
    """Process documents into chunks for embedding"""
    
    def __init__(self):
        """Initialize with text splitter"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.supported_extensions = config.SUPPORTED_FILE_TYPES
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load and chunk a single document"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        if file_extension not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        print(f"📄 Loading: {file_path.name}")
        
        # Load based on file type
        if file_extension == ".pdf":
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
    
    def load_documents(self, file_paths: List[str]) -> List[Document]:
        """Load and chunk multiple documents"""
        all_chunks = []
        
        print(f"\n📚 Loading {len(file_paths)} document(s)...")
        print("=" * 60)
        
        for file_path in file_paths:
            try:
                chunks = self.load_document(file_path)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"   ❌ Failed: {file_path} - {str(e)}")
                continue
        
        print("=" * 60)
        print(f"✅ Total chunks: {len(all_chunks)}")
        
        return all_chunks