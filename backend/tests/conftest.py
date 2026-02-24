"""
Pytest configuration and fixtures for backend tests.

This module provides test fixtures to mock services during testing.
"""

import pytest
from unittest.mock import MagicMock


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(monkeypatch_session):
    """
    Set up test environment by mocking slow operations.
    
    This runs once per test session to speed up tests.
    """
    # Mock the initialize_rag_system to return immediately
    async def mock_initialize_rag(*args, **kwargs):
        return {
            "success": True,
            "message": "Test mode - RAG not initialized",
            "chunks_processed": 0,
            "embeddings_generated": 0
        }
    
    import src.main
    src.main.initialize_rag_system = mock_initialize_rag


@pytest.fixture(scope="session")
def monkeypatch_session():
    """Session-scoped monkeypatch fixture."""
    from _pytest.monkeypatch import MonkeyPatch
    m = MonkeyPatch()
    yield m
    m.undo()
