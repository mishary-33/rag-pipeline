"""
Embeddings Module
Generate embeddings from document chunks using Google Gemini
"""

import warnings
warnings.filterwarnings('ignore')

import time
from typing import List
from google import genai
from src.config import config


class EmbeddingGenerator:
    """Generate embeddings using Google Gemini"""
    
    def __init__(self):
        """Initialize embedding generator"""
        self.client = genai.Client(api_key=config.GOOGLE_API_KEY)
        self.model = config.EMBEDDING_MODEL
        print(f"✅ Embedding model: {self.model}")
    
    def generate_embedding(self, text: str, retry_count: int = 3) -> List[float]:
        """
        Generate embedding for a single text with retry logic

        Args:
            text: Text to embed
            retry_count: Number of retries on rate limit errors

        Returns:
            List of floats (embedding vector)
        """
        from google.genai.errors import ClientError

        for attempt in range(retry_count):
            try:
                result = self.client.models.embed_content(
                    model=self.model,
                    contents=text
                )
                return result.embeddings[0].values
            except ClientError as e:
                # Check if this is a rate limit error (429)
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < retry_count - 1:
                        # Extract wait time from error message or use default
                        wait_time = 60  # Default wait time in seconds
                        print(f"\n⏳ Rate limit hit. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                    else:
                        raise
                else:
                    raise
    
    def generate_embeddings_batch(self, texts: List[str], delay: float = 0.6) -> List[List[float]]:
        """
        Generate embeddings for multiple texts with rate limiting

        Args:
            texts: List of texts to embed
            delay: Delay in seconds between requests (default 0.6s = ~100 requests/min)

        Returns:
            List of embedding vectors
        """
        embeddings = []
        total = len(texts)

        print(f"\n🔄 Generating embeddings for {total} chunks...")
        print(f"   (Rate limit: ~{int(60/delay)} requests/min)")

        for i, text in enumerate(texts, 1):
            if i % 10 == 0 or i == total:
                print(f"   Progress: {i}/{total}")

            embedding = self.generate_embedding(text)
            embeddings.append(embedding)

            # Add delay between requests to respect rate limits (except for last item)
            if i < total:
                time.sleep(delay)

        print(f"✅ Generated {len(embeddings)} embeddings")
        return embeddings
    
    def embed_documents(self, chunks):
        """
        Generate embeddings for document chunks
        
        Args:
            chunks: Document chunks from DocumentProcessor
            
        Returns:
            Tuple of (texts, embeddings, metadatas)
        """
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        embeddings = self.generate_embeddings_batch(texts)
        
        return texts, embeddings, metadatas