"""Groq client for LLM API calls with streaming support."""

import logging
from typing import AsyncGenerator, Optional

from groq import AsyncGroq

from ..config import settings

logger = logging.getLogger(__name__)


class GroqClient:
    """Client for Groq API with streaming support.
    
    This client provides a fallback LLM service when OpenRouter fails.
    Uses Groq's fast inference API with async streaming support.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq client with API key.
        
        Args:
            api_key: Groq API key. If not provided, uses settings.groq_api_key.
        
        Raises:
            ValueError: If API key is not provided and not in settings.
        """
        self.api_key = api_key or settings.groq_api_key
        if not self.api_key:
            raise ValueError("Groq API key is required")
        
        self.client = AsyncGroq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"  # Fastest free model
        
        logger.info("GroqClient initialized")

    async def stream_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> AsyncGenerator[str, None]:
        """Stream completion from Groq API.
        
        This method sends a prompt to the Groq API and streams the response
        back. It matches the OpenRouterClient interface for easy fallback.
        
        Args:
            prompt: The prompt to send to the LLM.
            temperature: Sampling temperature (0.0 to 1.0). Higher values make output
                        more random. Defaults to 0.7.
            max_tokens: Maximum number of tokens to generate. Defaults to 500.
        
        Yields:
            Response tokens as they arrive from the API.
        
        Raises:
            Exception: If API call fails.
        """
        try:
            logger.info("Sending request to Groq API")
            
            # Create streaming chat completion
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Stream response tokens
            token_count = 0
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        token_count += 1
                        yield delta.content
            
            logger.info(f"Groq stream completed ({token_count} tokens)")
        
        except Exception as e:
            logger.error(f"Groq API error: {e}", exc_info=True)
            raise
