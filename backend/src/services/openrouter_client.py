"""OpenRouter client for LLM API calls with streaming support."""

import asyncio
import json
import logging
from typing import AsyncGenerator, Optional

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """Client for OpenRouter API with streaming support and retry logic.
    
    This client handles:
    - Async HTTP requests to OpenRouter API
    - Server-Sent Events (SSE) streaming response parsing
    - Exponential backoff retry logic (3 attempts: 1s, 2s, 4s)
    - Rate limiting (429) and timeout error handling
    - 30-second timeout for requests
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenRouter client with API key.
        
        Args:
            api_key: OpenRouter API key. If not provided, uses settings.openrouter_api_key.
        
        Raises:
            ValueError: If API key is not provided and not in settings.
        """
        self.api_key = api_key or settings.openrouter_api_key
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "meta-llama/llama-3.1-8b-instruct:free"
        self.timeout = 30.0  # 30 seconds timeout
        self.max_retries = 3
        self.retry_delays = [1.0, 2.0, 4.0]  # Exponential backoff delays
        
        logger.info("OpenRouterClient initialized")

    def _get_headers(self) -> dict:
        """Get HTTP headers for OpenRouter API requests.
        
        Returns:
            Dictionary of HTTP headers including authorization.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://rushikesh-portfolio.vercel.app",  # Optional but recommended
            "X-Title": "AI Portfolio Chat Assistant"  # Optional but recommended
        }

    async def stream_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> AsyncGenerator[str, None]:
        """Stream completion from OpenRouter API with retry logic.
        
        This method sends a prompt to the OpenRouter API and streams the response
        back as Server-Sent Events (SSE). It implements exponential backoff retry
        for transient failures and handles rate limiting gracefully.
        
        Args:
            prompt: The prompt to send to the LLM.
            temperature: Sampling temperature (0.0 to 1.0). Higher values make output
                        more random. Defaults to 0.7.
            max_tokens: Maximum number of tokens to generate. Defaults to 500.
        
        Yields:
            Response tokens as they arrive from the API.
        
        Raises:
            httpx.HTTPError: If all retry attempts fail.
            asyncio.TimeoutError: If request exceeds timeout.
        """
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    # Prepare request payload
                    payload = {
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "stream": True
                    }
                    
                    logger.info(
                        f"Sending request to OpenRouter (attempt {attempt + 1}/{self.max_retries})"
                    )
                    
                    # Make streaming request
                    async with client.stream(
                        "POST",
                        f"{self.base_url}/chat/completions",
                        headers=self._get_headers(),
                        json=payload
                    ) as response:
                        # Check for rate limiting
                        if response.status_code == 429:
                            retry_after = response.headers.get("retry-after", "60")
                            logger.warning(
                                f"Rate limited (429). Retry after {retry_after} seconds"
                            )
                            
                            # If this is not the last attempt, wait and retry
                            if attempt < self.max_retries - 1:
                                delay = self.retry_delays[attempt]
                                logger.info(f"Waiting {delay}s before retry...")
                                await asyncio.sleep(delay)
                                continue
                            else:
                                response.raise_for_status()
                        
                        # Check for other HTTP errors
                        if response.status_code != 200:
                            logger.error(
                                f"OpenRouter API error: {response.status_code} - {response.text}"
                            )
                            
                            # If this is not the last attempt, wait and retry
                            if attempt < self.max_retries - 1:
                                delay = self.retry_delays[attempt]
                                logger.info(f"Waiting {delay}s before retry...")
                                await asyncio.sleep(delay)
                                continue
                            else:
                                response.raise_for_status()
                        
                        # Parse SSE stream
                        async for line in response.aiter_lines():
                            # SSE format: "data: {...}\n\n"
                            if line.startswith("data: "):
                                data_str = line[6:]  # Remove "data: " prefix
                                
                                # Check for stream end marker
                                if data_str.strip() == "[DONE]":
                                    logger.info("Stream completed successfully")
                                    return
                                
                                try:
                                    # Parse JSON data
                                    data = json.loads(data_str)
                                    
                                    # Extract content from response
                                    if "choices" in data and len(data["choices"]) > 0:
                                        choice = data["choices"][0]
                                        
                                        # Check for delta content (streaming format)
                                        if "delta" in choice and "content" in choice["delta"]:
                                            content = choice["delta"]["content"]
                                            if content:
                                                yield content
                                        
                                        # Check for finish reason
                                        if choice.get("finish_reason") == "stop":
                                            logger.info("Stream finished (stop reason)")
                                            return
                                
                                except json.JSONDecodeError as e:
                                    logger.warning(f"Failed to parse SSE data: {e}")
                                    continue
                        
                        # If we reach here, stream completed successfully
                        logger.info("Stream completed")
                        return
            
            except httpx.TimeoutException as e:
                logger.error(f"Request timeout (attempt {attempt + 1}/{self.max_retries}): {e}")
                
                # If this is not the last attempt, wait and retry
                if attempt < self.max_retries - 1:
                    delay = self.retry_delays[attempt]
                    logger.info(f"Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise
            
            except httpx.HTTPError as e:
                logger.error(f"HTTP error (attempt {attempt + 1}/{self.max_retries}): {e}")
                
                # If this is not the last attempt, wait and retry
                if attempt < self.max_retries - 1:
                    delay = self.retry_delays[attempt]
                    logger.info(f"Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise
            
            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}/{self.max_retries}): {e}")
                
                # If this is not the last attempt, wait and retry
                if attempt < self.max_retries - 1:
                    delay = self.retry_delays[attempt]
                    logger.info(f"Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise
        
        # This should never be reached, but just in case
        raise Exception("All retry attempts exhausted")
