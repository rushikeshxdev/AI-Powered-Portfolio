"""Unit tests for VectorStore service."""

import tempfile
from pathlib import Path

import pytest

from src.services.vector_store import VectorStore


@pytest.fixture
def temp_chroma_dir():
    """Create a temporary directory for ChromaDB storage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def vector_store(temp_chroma_dir):
    """Create a VectorStore instance with temporary storage."""
    return VectorStore(persist_directory=temp_chroma_dir, collection_name="test_collection")


@pytest.fixture
def sample_embeddings():
    """Generate sample 384-dimensional embeddings."""
    return [
        [0.1] * 384,
        [0.2] * 384,
        [0.3] * 384,
    ]


@pytest.fixture
def sample_texts():
    """Generate sample text chunks."""
    return [
        "This is the first document about Python programming.",
        "This is the second document about web development.",
        "This is the third document about machine learning.",
    ]


@pytest.fixture
def sample_metadatas():
    """Generate sample metadata."""
    return [
        {"section": "skills", "subsection": "languages"},
        {"section": "projects", "subsection": "project_1"},
        {"section": "experience", "subsection": "current_role"},
    ]


class TestVectorStoreInitialization:
    """Tests for VectorStore initialization."""

    def test_initialization_creates_directory(self, temp_chroma_dir):
        """Test that initialization creates the persist directory."""
        persist_path = Path(temp_chroma_dir) / "new_dir"
        vector_store = VectorStore(persist_directory=str(persist_path))
        
        assert persist_path.exists()
        assert vector_store.client is not None
        assert vector_store.collection_name == "resume_chunks"

    def test_initialization_with_custom_collection_name(self, temp_chroma_dir):
        """Test initialization with custom collection name."""
        vector_store = VectorStore(
            persist_directory=temp_chroma_dir,
            collection_name="custom_collection"
        )
        
        assert vector_store.collection_name == "custom_collection"

    def test_initialization_with_existing_directory(self, temp_chroma_dir):
        """Test that initialization works with existing directory."""
        # Create first instance
        vector_store1 = VectorStore(persist_directory=temp_chroma_dir)
        
        # Create second instance with same directory
        vector_store2 = VectorStore(persist_directory=temp_chroma_dir)
        
        assert vector_store2.client is not None


class TestAddDocuments:
    """Tests for add_documents method."""

    def test_add_documents_basic(self, vector_store, sample_texts, sample_embeddings):
        """Test adding documents with texts and embeddings."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        count = vector_store.get_collection_count()
        assert count == 3

    def test_add_documents_with_metadata(
        self, vector_store, sample_texts, sample_embeddings, sample_metadatas
    ):
        """Test adding documents with metadata."""
        vector_store.add_documents(sample_texts, sample_embeddings, sample_metadatas)
        
        count = vector_store.get_collection_count()
        assert count == 3

    def test_add_documents_mismatched_lengths(self, vector_store, sample_texts):
        """Test that mismatched lengths raise ValueError."""
        embeddings = [[0.1] * 384]  # Only one embedding
        
        with pytest.raises(ValueError, match="must match number of embeddings"):
            vector_store.add_documents(sample_texts, embeddings)

    def test_add_documents_mismatched_metadata_length(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test that mismatched metadata length raises ValueError."""
        metadatas = [{"key": "value"}]  # Only one metadata
        
        with pytest.raises(ValueError, match="must match number of texts"):
            vector_store.add_documents(sample_texts, sample_embeddings, metadatas)

    def test_add_documents_wrong_embedding_dimension(self, vector_store, sample_texts):
        """Test that wrong embedding dimensions raise ValueError."""
        wrong_embeddings = [[0.1] * 128, [0.2] * 128, [0.3] * 128]  # Wrong dimension
        
        with pytest.raises(ValueError, match="must be 384-dimensional"):
            vector_store.add_documents(sample_texts, wrong_embeddings)

    def test_add_documents_empty_lists(self, vector_store):
        """Test adding empty lists."""
        vector_store.add_documents([], [])
        
        count = vector_store.get_collection_count()
        assert count == 0

    def test_add_documents_creates_collection(self, temp_chroma_dir, sample_texts, sample_embeddings):
        """Test that add_documents creates collection if it doesn't exist."""
        vector_store = VectorStore(persist_directory=temp_chroma_dir)
        
        # Collection should not exist yet
        assert vector_store.collection is None
        
        # Add documents should create collection
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        assert vector_store.collection is not None
        assert vector_store.get_collection_count() == 3


class TestSimilaritySearch:
    """Tests for similarity_search method."""

    def test_similarity_search_basic(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test basic similarity search."""
        # Add documents first
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        # Search with first embedding
        query_embedding = [0.1] * 384
        results = vector_store.similarity_search(query_embedding, k=2)
        
        assert len(results) == 2
        assert all(isinstance(text, str) for text, _ in results)
        assert all(isinstance(score, float) for _, score in results)

    def test_similarity_search_returns_top_k(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test that similarity search returns at most k results."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        # Request more results than available
        results = vector_store.similarity_search([0.1] * 384, k=10)
        
        # Should return only 3 (number of documents)
        assert len(results) <= 3

    def test_similarity_search_ordered_by_score(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test that results are ordered by similarity score."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        results = vector_store.similarity_search([0.1] * 384, k=3)
        
        # Extract scores
        scores = [score for _, score in results]
        
        # Scores should be in descending order
        assert scores == sorted(scores, reverse=True)

    def test_similarity_search_empty_collection(self, vector_store):
        """Test similarity search on empty collection."""
        results = vector_store.similarity_search([0.1] * 384, k=3)
        
        assert results == []

    def test_similarity_search_wrong_embedding_dimension(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test that wrong query embedding dimension raises ValueError."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        wrong_embedding = [0.1] * 128  # Wrong dimension
        
        with pytest.raises(ValueError, match="must be 384-dimensional"):
            vector_store.similarity_search(wrong_embedding, k=3)

    def test_similarity_search_invalid_k(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test that k < 1 raises ValueError."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        with pytest.raises(ValueError, match="k must be at least 1"):
            vector_store.similarity_search([0.1] * 384, k=0)

    def test_similarity_search_k_equals_one(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test similarity search with k=1."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        results = vector_store.similarity_search([0.1] * 384, k=1)
        
        assert len(results) == 1

    def test_similarity_search_nonexistent_collection(self, temp_chroma_dir):
        """Test similarity search when collection doesn't exist."""
        vector_store = VectorStore(persist_directory=temp_chroma_dir)
        
        results = vector_store.similarity_search([0.1] * 384, k=3)
        
        assert results == []


class TestClearCollection:
    """Tests for clear_collection method."""

    def test_clear_collection(self, vector_store, sample_texts, sample_embeddings):
        """Test clearing collection."""
        # Add documents
        vector_store.add_documents(sample_texts, sample_embeddings)
        assert vector_store.get_collection_count() == 3
        
        # Clear collection
        vector_store.clear_collection()
        
        # Collection should be None after clearing
        assert vector_store.collection is None

    def test_clear_empty_collection(self, vector_store):
        """Test clearing an empty collection."""
        # Should not raise error
        vector_store.clear_collection()
        
        assert vector_store.collection is None


class TestGetCollectionCount:
    """Tests for get_collection_count method."""

    def test_get_collection_count_with_documents(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test getting count with documents."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        count = vector_store.get_collection_count()
        
        assert count == 3

    def test_get_collection_count_empty(self, vector_store):
        """Test getting count of empty collection."""
        count = vector_store.get_collection_count()
        
        assert count == 0

    def test_get_collection_count_nonexistent_collection(self, temp_chroma_dir):
        """Test getting count when collection doesn't exist."""
        vector_store = VectorStore(persist_directory=temp_chroma_dir)
        
        count = vector_store.get_collection_count()
        
        assert count == 0


class TestPersistence:
    """Tests for data persistence."""

    def test_persistence_across_instances(
        self, temp_chroma_dir, sample_texts, sample_embeddings
    ):
        """Test that data persists across VectorStore instances."""
        # Create first instance and add documents
        vector_store1 = VectorStore(
            persist_directory=temp_chroma_dir,
            collection_name="persist_test"
        )
        vector_store1.add_documents(sample_texts, sample_embeddings)
        
        # Create second instance with same directory and collection
        vector_store2 = VectorStore(
            persist_directory=temp_chroma_dir,
            collection_name="persist_test"
        )
        
        # Should be able to search in second instance
        results = vector_store2.similarity_search([0.1] * 384, k=3)
        
        assert len(results) == 3


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_add_documents_with_special_characters(self, vector_store):
        """Test adding documents with special characters."""
        texts = [
            "Document with special chars: @#$%^&*()",
            "Document with unicode: 你好世界",
            "Document with newlines:\nLine 1\nLine 2",
        ]
        embeddings = [[0.1] * 384, [0.2] * 384, [0.3] * 384]
        
        vector_store.add_documents(texts, embeddings)
        
        assert vector_store.get_collection_count() == 3

    def test_similarity_search_with_zero_vector(
        self, vector_store, sample_texts, sample_embeddings
    ):
        """Test similarity search with zero vector."""
        vector_store.add_documents(sample_texts, sample_embeddings)
        
        zero_embedding = [0.0] * 384
        results = vector_store.similarity_search(zero_embedding, k=3)
        
        # Should still return results
        assert len(results) > 0

    def test_add_documents_with_empty_strings(self, vector_store):
        """Test adding documents with empty strings."""
        texts = ["", "Valid text", ""]
        embeddings = [[0.1] * 384, [0.2] * 384, [0.3] * 384]
        
        # Should not raise error
        vector_store.add_documents(texts, embeddings)
        
        assert vector_store.get_collection_count() == 3

    def test_multiple_collections_same_directory(self, temp_chroma_dir, sample_texts, sample_embeddings):
        """Test multiple collections in the same directory."""
        # Create two vector stores with different collection names
        vector_store1 = VectorStore(
            persist_directory=temp_chroma_dir,
            collection_name="collection1"
        )
        vector_store2 = VectorStore(
            persist_directory=temp_chroma_dir,
            collection_name="collection2"
        )
        
        # Add documents to both
        vector_store1.add_documents(sample_texts, sample_embeddings)
        vector_store2.add_documents(sample_texts[:2], sample_embeddings[:2])
        
        # Each should have independent counts
        assert vector_store1.get_collection_count() == 3
        assert vector_store2.get_collection_count() == 2
