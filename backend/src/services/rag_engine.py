"""RAG Engine for orchestrating the complete RAG pipeline."""

import logging
from typing import AsyncGenerator, List, Tuple

from .embedding_service import EmbeddingService
from .openrouter_client import OpenRouterClient
from .vector_store import VectorStore

logger = logging.getLogger(__name__)


class RAGEngine:
    """RAG Engine that orchestrates the complete RAG pipeline.
    
    This engine coordinates:
    1. Question embedding generation using EmbeddingService
    2. Similarity search in VectorStore for relevant context
    3. Prompt construction with system message, context, and question
    4. Streaming LLM response using OpenRouterClient
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        openrouter_client: OpenRouterClient
    ):
        """Initialize RAG Engine with required services.
        
        Args:
            embedding_service: Service for generating embeddings.
            vector_store: Vector store for similarity search.
            openrouter_client: Client for OpenRouter API.
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.openrouter_client = openrouter_client
        
        logger.info("RAGEngine initialized successfully")

    def _construct_prompt(
        self,
        question: str,
        context_chunks: List[str]
    ) -> str:
        """Construct prompt with system message, context, and question.
        
        The prompt format follows the specification:
        - System message explaining the assistant's role
        - Context section with retrieved resume chunks
        - User question
        
        Args:
            question: The user's question.
            context_chunks: List of relevant resume chunks from vector search.
        
        Returns:
            Formatted prompt string ready for LLM.
        """
        # System message
        system_message = (
            "You are a helpful AI assistant answering questions about "
            "Rushikesh Randive's portfolio and experience. Use the provided "
            "context to answer accurately."
        )
        
        # Format context chunks
        context_section = "\n".join(
            f"[{i+1}] {chunk}" for i, chunk in enumerate(context_chunks)
        )
        
        # Construct complete prompt
        prompt = f"""System: {system_message}

Context:
{context_section}

Question: {question}"""
        
        return prompt

    async def process_question(
        self,
        question: str
    ) -> AsyncGenerator[str, None]:
        """Process question through RAG pipeline and stream response.
        
        Pipeline steps:
        1. Generate embedding for the user's question
        2. Query VectorStore for top 3 most similar resume chunks
        3. Construct prompt with system message, context, and question
        4. Stream LLM response from OpenRouterClient
        
        Args:
            question: The user's question about the resume.
        
        Yields:
            Response tokens as they arrive from the LLM.
        
        Raises:
            ValueError: If question is empty.
            Exception: If any pipeline step fails.
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            # Step 1: Generate question embedding
            logger.info(f"Generating embedding for question: {question[:50]}...")
            question_embedding = self.embedding_service.generate_embedding(question)
            logger.info(f"Generated embedding with dimension: {len(question_embedding)}")
            
            # Step 2: Query vector store for top 3 similar chunks
            logger.info("Querying vector store for similar chunks...")
            results = self.vector_store.similarity_search(
                query_embedding=question_embedding,
                k=3
            )
            
            # Extract text chunks from results
            context_chunks = [text for text, score in results]
            logger.info(f"Retrieved {len(context_chunks)} context chunks")
            
            # Log similarity scores for debugging
            for i, (text, score) in enumerate(results):
                logger.debug(f"Chunk {i+1} similarity: {score:.4f} - {text[:100]}...")
            
            # Step 3: Construct prompt
            logger.info("Constructing prompt with context...")
            prompt = self._construct_prompt(question, context_chunks)
            logger.debug(f"Prompt length: {len(prompt)} characters")
            
            # Step 4: Stream LLM response
            logger.info("Streaming response from OpenRouter...")
            token_count = 0
            async for token in self.openrouter_client.stream_completion(prompt):
                token_count += 1
                yield token
            
            logger.info(f"Completed streaming response ({token_count} tokens)")
        
        except ValueError as e:
            logger.error(f"Validation error in RAG pipeline: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}", exc_info=True)
            raise
