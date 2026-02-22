"""Tests for RAGEngine."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from src.services.rag_engine import RAGEngine
from src.services.embedding_service import EmbeddingService
from src.services.vector_store import VectorStore
from src.services.openrouter_client import OpenRouterClient


@pytest.fixture
def mock_embedding_service():
    """Create a mock EmbeddingService."""
    service = Mock(spec=EmbeddingService)
    # Mock generate_embedding to return a 384-dimensional vector
    service.generate_embedding.return_value = [0.1] * 384
    return service


@pytest.fixture
def mock_vector_store():
    """Create a mock VectorStore."""
    store = Mock(spec=VectorStore)
    # Mock similarity_search to return 3 chunks with scores
    store.similarity_search.return_value = [
        ("Rushikesh Randive is a Computer Science student at KIT College. Contact: rushikesh@example.com, LinkedIn: linkedin.com/in/rushikesh", 0.95),
        ("Programming Languages: Python, JavaScript, TypeScript, Java, C++, SQL", 0.87),
        ("AI Portfolio with RAG Chat: Interactive portfolio website with AI-powered chat assistant. Built with React, TypeScript, FastAPI, ChromaDB.", 0.82)
    ]
    return store


@pytest.fixture
def mock_openrouter_client():
    """Create a mock OpenRouterClient."""
    client = Mock(spec=OpenRouterClient)
    
    # Create an async generator for streaming
    async def mock_stream():
        tokens = ["Hello", " ", "there", "!", " ", "I", " ", "can", " ", "help", "."]
        for token in tokens:
            yield token
    
    client.stream_completion = AsyncMock(return_value=mock_stream())
    return client


@pytest.fixture
def rag_engine(mock_embedding_service, mock_vector_store, mock_openrouter_client):
    """Create a RAGEngine instance with mocked dependencies."""
    return RAGEngine(
        embedding_service=mock_embedding_service,
        vector_store=mock_vector_store,
        openrouter_client=mock_openrouter_client
    )


class TestRAGEngineInitialization:
    """Tests for RAGEngine initialization."""

    def test_initialization_with_services(self, mock_embedding_service, mock_vector_store, mock_openrouter_client):
        """Test that RAGEngine initializes with required services."""
        engine = RAGEngine(
            embedding_service=mock_embedding_service,
            vector_store=mock_vector_store,
            openrouter_client=mock_openrouter_client
        )
        
        assert engine.embedding_service == mock_embedding_service
        assert engine.vector_store == mock_vector_store
        assert engine.openrouter_client == mock_openrouter_client


class TestConstructPrompt:
    """Tests for _construct_prompt method."""

    def test_construct_prompt_with_context(self, rag_engine):
        """Test prompt construction with context chunks."""
        question = "What projects has Rushikesh worked on?"
        context_chunks = [
            "AI Portfolio with RAG Chat: Interactive portfolio website.",
            "Task Management System: Full-stack application with real-time updates.",
            "E-commerce Platform: Modern platform with payment integration."
        ]
        
        prompt = rag_engine._construct_prompt(question, context_chunks)
        
        # Check that prompt contains all required parts
        assert "System:" in prompt
        assert "Rushikesh Randive's portfolio and experience" in prompt
        assert "Context:" in prompt
        assert "Question:" in prompt
        assert question in prompt
        
        # Check that all context chunks are included
        for chunk in context_chunks:
            assert chunk in prompt

    def test_construct_prompt_with_empty_context(self, rag_engine):
        """Test prompt construction with empty context."""
        question = "Tell me about Rushikesh"
        context_chunks = []
        
        prompt = rag_engine._construct_prompt(question, context_chunks)
        
        assert "System:" in prompt
        assert "Context:" in prompt
        assert "Question:" in prompt
        assert question in prompt

    def test_construct_prompt_formats_chunks_with_numbers(self, rag_engine):
        """Test that context chunks are numbered."""
        question = "What skills does Rushikesh have?"
        context_chunks = [
            "Python, JavaScript, TypeScript",
            "React, Vue.js, Tailwind CSS",
            "FastAPI, Node.js, Express"
        ]
        
        prompt = rag_engine._construct_prompt(question, context_chunks)
        
        # Check that chunks are numbered [1], [2], [3]
        assert "[1]" in prompt
        assert "[2]" in prompt
        assert "[3]" in prompt


class TestProcessQuestion:
    """Tests for process_question method."""

    @pytest.mark.asyncio
    async def test_process_question_with_valid_input(self, rag_engine, mock_embedding_service, mock_vector_store, mock_openrouter_client):
        """Test processing a valid question through the RAG pipeline."""
        question = "What projects has Rushikesh worked on?"
        
        # Create a proper async generator for the mock
        async def mock_stream():
            tokens = ["AI", " ", "Portfolio", " ", "project"]
            for token in tokens:
                yield token
        
        mock_openrouter_client.stream_completion = AsyncMock(return_value=mock_stream())
        
        # Process question and collect response
        response_tokens = []
        async for token in rag_engine.process_question(question):
            response_tokens.append(token)
        
        # Verify the pipeline was executed
        mock_embedding_service.generate_embedding.assert_called_once_with(question)
        mock_vector_store.similarity_search.assert_called_once()
        mock_openrouter_client.stream_completion.assert_called_once()
        
        # Verify response was streamed
        assert len(response_tokens) > 0
        assert "".join(response_tokens) == "AI Portfolio project"

    @pytest.mark.asyncio
    async def test_process_question_calls_embedding_service(self, rag_engine, mock_embedding_service):
        """Test that process_question calls embedding service."""
        question = "Tell me about Rushikesh's education"
        
        # Create a proper async generator
        async def mock_stream():
            yield "Response"
        
        rag_engine.openrouter_client.stream_completion = AsyncMock(return_value=mock_stream())
        
        # Process question
        async for _ in rag_engine.process_question(question):
            pass
        
        # Verify embedding service was called with the question
        mock_embedding_service.generate_embedding.assert_called_once_with(question)

    @pytest.mark.asyncio
    async def test_process_question_queries_vector_store(self, rag_engine, mock_vector_store):
        """Test that process_question queries vector store with k=3."""
        question = "What technologies does Rushikesh know?"
        
        # Create a proper async generator
        async def mock_stream():
            yield "Response"
        
        rag_engine.openrouter_client.stream_completion = AsyncMock(return_value=mock_stream())
        
        # Process question
        async for _ in rag_engine.process_question(question):
            pass
        
        # Verify vector store was queried with k=3
        mock_vector_store.similarity_search.assert_called_once()
        call_args = mock_vector_store.similarity_search.call_args
        assert call_args.kwargs.get('k') == 3

    @pytest.mark.asyncio
    async def test_process_question_with_empty_string_raises_error(self, rag_engine):
        """Test that empty question raises ValueError."""
        with pytest.raises(ValueError, match="Question cannot be empty"):
            async for _ in rag_engine.process_question(""):
                pass

    @pytest.mark.asyncio
    async def test_process_question_with_whitespace_only_raises_error(self, rag_engine):
        """Test that whitespace-only question raises ValueError."""
        with pytest.raises(ValueError, match="Question cannot be empty"):
            async for _ in rag_engine.process_question("   "):
                pass

    @pytest.mark.asyncio
    async def test_process_question_constructs_prompt_with_context(self, rag_engine, mock_openrouter_client):
        """Test that process_question constructs prompt with retrieved context."""
        question = "What is Rushikesh's current role?"
        
        # Create a proper async generator
        async def mock_stream():
            yield "Response"
        
        mock_openrouter_client.stream_completion = AsyncMock(return_value=mock_stream())
        
        # Process question
        async for _ in rag_engine.process_question(question):
            pass
        
        # Verify OpenRouter client was called with a prompt
        mock_openrouter_client.stream_completion.assert_called_once()
        call_args = mock_openrouter_client.stream_completion.call_args
        prompt = call_args[0][0]  # First positional argument
        
        # Verify prompt contains system message, context, and question
        assert "System:" in prompt
        assert "Context:" in prompt
        assert "Question:" in prompt
        assert question in prompt

    @pytest.mark.asyncio
    async def test_process_question_streams_response(self, rag_engine):
        """Test that process_question streams response tokens."""
        question = "Tell me about Rushikesh"
        
        # Create a proper async generator with multiple tokens
        async def mock_stream():
            tokens = ["Hello", " ", "world", "!"]
            for token in tokens:
                yield token
        
        rag_engine.openrouter_client.stream_completion = AsyncMock(return_value=mock_stream())
        
        # Collect streamed tokens
        tokens = []
        async for token in rag_engine.process_question(question):
            tokens.append(token)
        
        # Verify tokens were streamed
        assert len(tokens) == 4
        assert "".join(tokens) == "Hello world!"

    @pytest.mark.asyncio
    async def test_process_question_handles_no_context_results(self, rag_engine, mock_vector_store):
        """Test handling when vector store returns no results."""
        question = "Random question"
        
        # Mock vector store to return empty results
        mock_vector_store.similarity_search.return_value = []
        
        # Create a proper async generator
        async def mock_stream():
            yield "No information available"
        
        rag_engine.openrouter_client.stream_completion = AsyncMock(return_value=mock_stream())
        
        # Process question
        response_tokens = []
        async for token in rag_engine.process_question(question):
            response_tokens.append(token)
        
        # Should still work with empty context
        assert len(response_tokens) > 0


class TestIntegration:
    """Integration tests for RAGEngine."""

    @pytest.mark.asyncio
    async def test_complete_rag_pipeline(self, rag_engine):
        """Test the complete RAG pipeline from question to response."""
        question = "What projects has Rushikesh worked on?"
        
        # Create a proper async generator
        async def mock_stream():
            response = "Rushikesh has worked on several projects including an AI Portfolio with RAG Chat."
            for word in response.split():
                yield word + " "
        
        rag_engine.openrouter_client.stream_completion = AsyncMock(return_value=mock_stream())
        
        # Process question
        response_tokens = []
        async for token in rag_engine.process_question(question):
            response_tokens.append(token)
        
        # Verify complete response
        response = "".join(response_tokens)
        assert len(response) > 0
        assert "Rushikesh" in response or "projects" in response or "AI" in response
