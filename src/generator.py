"""
Generator Module
Generate answers using Google Gemini based on retrieved context
"""

import warnings
warnings.filterwarnings('ignore')

from google import genai
from src.config import config
from typing import List, Dict, Generator as Gen


class ResponseGenerator:
    """Generate responses using Google Gemini"""
    
    def __init__(self):
        """Initialize generator"""
        self.client = genai.Client(api_key=config.GOOGLE_API_KEY)
        self.model = config.LLM_MODEL
        print(f"✅ Generator model: {self.model}")
    
    def check_relevance(self, context_chunks: List[Dict], threshold: float = 0.5) -> bool:
        """
        Check if retrieved chunks are relevant enough
        
        Args:
            context_chunks: Retrieved chunks with distances
            threshold: Maximum distance for relevance (lower = more similar)
            
        Returns:
            True if chunks seem relevant, False otherwise
        """
        if not context_chunks:
            return False
        
        # Check if best result is below threshold
        best_distance = context_chunks[0].get('distance', 1.0)
        
        return best_distance < threshold

    def create_prompt(self, query: str, context_chunks: List[Dict], chat_history: List[Dict] = None) -> str:
        """Create prompt with context and chat history"""
        # Build context from chunks
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            source = chunk['metadata'].get('source_file', 'Unknown')
            page = chunk['metadata'].get('page', 'N/A')
            text = chunk['text']
            
            context_parts.append(
                f"[Document {i}] (Source: {source}, Page: {page})\n{text}\n"
            )
        
        context = "\n".join(context_parts)
        
        # Build conversation history
        history_text = ""
        if chat_history and len(chat_history) > 0:
            history_text = "Previous conversation:\n"
            for msg in chat_history[-6:]:  # Last 3 exchanges (6 messages)
                role = "User" if msg["role"] == "user" else "Assistant"
                content = msg["content"]
                history_text += f"{role}: {content}\n"
            history_text += "\n"
        
        # Create prompt
        prompt = f"""You are a knowledgeable research assistant analyzing documents. Answer the user's question thoroughly based on the provided context and conversation history.

{history_text}Context from documents:
{context}

Current Question: {query}

Instructions:
- Consider the conversation history when answering
- If this is a follow-up question, refer back to previous context
- Provide comprehensive, detailed answers using the information from the documents
- Include specific details, examples, and explanations from the context
- Cite sources using document numbers (e.g., "According to Document 1...")
- If information spans multiple documents, synthesize them coherently
- If the documents are in Arabic and the question is in Arabic, answer in Arabic
- If the documents are in Arabic but question is in English, answer in English
- If the answer cannot be found in the documents, clearly state: "I cannot find this information in the provided documents."
- Aim for 3-5 paragraphs for complex questions
- Do not include punctionations when answering in arabic 

Answer:"""
        
        return prompt
    
    def generate(self, query: str, context_chunks: List[Dict], chat_history: List[Dict] = None) -> str:
        """Generate non-streaming response"""

        if not self.check_relevance(context_chunks, threshold=0.6):
            return "⚠️ I cannot find relevant information about this question in the provided documents. The available documents may not cover this topic."

        prompt = self.create_prompt(query, context_chunks, chat_history)
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        return response.text
    
    def generate_stream(self, query: str, context_chunks: List[Dict], chat_history: List[Dict] = None) -> Gen[str, None, None]:
        """Generate streaming response"""
        
        if not self.check_relevance(context_chunks, threshold=0.39):
            yield "⚠️ I cannot find relevant information..."
            return

        prompt = self.create_prompt(query, context_chunks, chat_history)
        
        response = self.client.models.generate_content_stream(
            model=self.model,
            contents=prompt
        )
        
        for chunk in response:
            if chunk.text:
                yield chunk.text