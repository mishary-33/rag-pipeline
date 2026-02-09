"""
Vector Store Module
Store and retrieve document embeddings using FAISS
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import faiss
import pickle
from typing import List, Tuple
from pathlib import Path


class VectorStore:
    """FAISS-based vector store for document embeddings"""
    
    def __init__(self, dimension: int = 3072):
        """Initialize vector store"""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []
        self.metadatas = []
        print(f"✅ Vector store initialized (dimension: {dimension})")
    
    def add_documents(self, texts: List[str], embeddings: List[List[float]], metadatas: List[dict]):
        """Add documents to the vector store"""
        print(f"\n📥 Adding {len(texts)} documents to vector store...")
        
        # Convert embeddings to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings_array)
        
        # Store texts and metadata
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)
        
        print(f"✅ Total documents in store: {self.index.ntotal}")
    
    def search(self, query_embedding: List[float], k: int = 5) -> List[Tuple[str, dict, float]]:
        """Search for similar documents"""
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search FAISS index
        distances, indices = self.index.search(query_array, k)
        
        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts):
                results.append({
                    'text': self.texts[idx],
                    'metadata': self.metadatas[idx],
                    'distance': float(distances[0][i])
                })
        
        return results
    
    def save(self, path: str):
        """Save vector store to disk"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(path / "index.faiss"))
        
        # Save texts and metadata
        with open(path / "data.pkl", "wb") as f:
            pickle.dump({
                'texts': self.texts,
                'metadatas': self.metadatas,
                'dimension': self.dimension
            }, f)
        
        print(f"✅ Vector store saved to {path}")
    
    def load(self, path: str):
        """Load vector store from disk"""
        path = Path(path)
        
        # Load FAISS index
        self.index = faiss.read_index(str(path / "index.faiss"))
        
        # Load texts and metadata
        with open(path / "data.pkl", "rb") as f:
            data = pickle.load(f)
            self.texts = data['texts']
            self.metadatas = data['metadatas']
            self.dimension = data['dimension']
        
        print(f"✅ Loaded {self.index.ntotal} documents from {path}")