"""
Embeddings Module - HuggingFace Version
Generate embeddings using local HuggingFace models (FREE, no API limits)
"""

import warnings
warnings.filterwarnings('ignore')

from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """Generate embeddings using HuggingFace models"""
    
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large"):
        """Initialize embedding generator
        used models but did not work: all-MiniLM-L6-v2, multilingual-e5-small, gemini embeding model.  
        """
        print(f"📥 Loading model: {model_name}")
        
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        print(f"✅ Model loaded (dimension: {self.dimension})")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        text = "query: " + text
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings for multiple texts (batched for speed)"""
        print(f"\n🔄 Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        print(f"✅ Generated {len(embeddings)} embeddings")
        return embeddings.tolist()
    
    def embed_documents(self, chunks):
        """Generate embeddings for document chunks"""
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        prefixed_texts = ["passage: " + t for t in texts]
        embeddings = self.generate_embeddings_batch(prefixed_texts)
        
        return texts, embeddings, metadatas