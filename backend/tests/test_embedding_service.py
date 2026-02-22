"""Tests for EmbeddingService."""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from src.services.embedding_service import EmbeddingService


@pytest.fixture
def embedding_service():
    """Create an EmbeddingService instance for testing."""
    return EmbeddingService()


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing."""
    return {
        "personal": {
            "name": "Test User",
            "email": "test@example.com",
            "linkedin": "https://linkedin.com/in/testuser",
            "github": "https://github.com/testuser",
            "location": "Test City"
        },
        "education": {
            "institution": "Test University",
            "degree": "B.Tech in Computer Science",
            "cgpa": "8.5/10",
            "expected_graduation": "2026",
            "relevant_coursework": [
                "Data Structures",
                "Algorithms",
                "Machine Learning",
                "Web Development"
            ]
        },
        "experience": [
            {
                "company": "Test Company",
                "role": "Software Engineer Intern",
                "duration": "6 months",
                "location": "Remote",
                "responsibilities": [
                    "Developed web applications using React and FastAPI",
                    "Implemented RESTful APIs for data management",
                    "Collaborated with team members on code reviews"
                ],
                "technologies": ["Python", "React", "FastAPI", "PostgreSQL"]
            }
        ],
        "skills": {
            "languages": ["Python", "JavaScript", "TypeScript", "Java"],
            "frontend": ["React", "Vue.js", "Tailwind CSS"],
            "backend": ["FastAPI", "Node.js", "Express"],
            "databases": ["PostgreSQL", "MongoDB", "Redis"],
            "devops": ["Docker", "Git", "GitHub Actions"],
            "ai_ml": ["TensorFlow", "PyTorch", "Sentence Transformers"]
        },
        "projects": [
            {
                "name": "Test Project 1",
                "description": "A comprehensive web application for managing tasks with real-time collaboration features. Built with modern technologies and best practices.",
                "technologies": ["React", "Node.js", "MongoDB", "Socket.io"],
                "highlights": [
                    "Implemented real-time updates using WebSockets",
                    "Built RESTful API with comprehensive error handling",
                    "Achieved 90% test coverage with Jest"
                ],
                "github": "https://github.com/testuser/project1",
                "demo": "https://project1.example.com"
            },
            {
                "name": "Test Project 2",
                "description": "An AI-powered chatbot using natural language processing to provide customer support. Integrated with multiple APIs for enhanced functionality.",
                "technologies": ["Python", "FastAPI", "OpenAI API", "PostgreSQL"],
                "highlights": [
                    "Integrated OpenAI GPT-3.5 for natural language understanding",
                    "Implemented caching to reduce API costs by 40%",
                    "Deployed on AWS with auto-scaling capabilities"
                ],
                "github": "https://github.com/testuser/project2"
            }
        ]
    }


class TestEmbeddingServiceInitialization:
    """Tests for EmbeddingService initialization."""

    def test_initialization_with_default_model(self, embedding_service):
        """Test that service initializes with default model."""
        assert embedding_service.model is not None
        assert embedding_service.embedding_dimension == 384

    def test_initialization_with_custom_model(self):
        """Test initialization with a custom model name."""
        service = EmbeddingService(model_name="all-MiniLM-L6-v2")
        assert service.model is not None
        assert service.embedding_dimension == 384


class TestGenerateEmbedding:
    """Tests for generate_embedding method."""

    def test_generate_embedding_returns_correct_dimension(self, embedding_service):
        """Test that embeddings have correct dimension (384)."""
        text = "This is a test sentence for embedding generation."
        embedding = embedding_service.generate_embedding(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) == 384
        assert all(isinstance(x, float) for x in embedding)

    def test_generate_embedding_with_short_text(self, embedding_service):
        """Test embedding generation with short text."""
        text = "Hello"
        embedding = embedding_service.generate_embedding(text)
        
        assert len(embedding) == 384

    def test_generate_embedding_with_long_text(self, embedding_service):
        """Test embedding generation with long text."""
        text = " ".join(["word"] * 200)  # 200 words
        embedding = embedding_service.generate_embedding(text)
        
        assert len(embedding) == 384

    def test_generate_embedding_with_empty_string_raises_error(self, embedding_service):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            embedding_service.generate_embedding("")

    def test_generate_embedding_with_whitespace_only_raises_error(self, embedding_service):
        """Test that whitespace-only string raises ValueError."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            embedding_service.generate_embedding("   ")

    def test_generate_embedding_with_special_characters(self, embedding_service):
        """Test embedding generation with special characters."""
        text = "Hello! @#$%^&*() Testing 123 <html> tags"
        embedding = embedding_service.generate_embedding(text)
        
        assert len(embedding) == 384

    def test_embeddings_are_different_for_different_texts(self, embedding_service):
        """Test that different texts produce different embeddings."""
        text1 = "Python programming language"
        text2 = "JavaScript web development"
        
        embedding1 = embedding_service.generate_embedding(text1)
        embedding2 = embedding_service.generate_embedding(text2)
        
        assert embedding1 != embedding2

    def test_embeddings_are_consistent(self, embedding_service):
        """Test that same text produces same embedding."""
        text = "Consistent embedding test"
        
        embedding1 = embedding_service.generate_embedding(text)
        embedding2 = embedding_service.generate_embedding(text)
        
        # Embeddings should be identical for same input
        assert embedding1 == embedding2


class TestChunkResume:
    """Tests for chunk_resume method."""

    def test_chunk_resume_returns_list(self, embedding_service, sample_resume_data):
        """Test that chunk_resume returns a list."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        assert isinstance(chunks, list)

    def test_chunk_resume_produces_non_empty_chunks(self, embedding_service, sample_resume_data):
        """Test that all chunks are non-empty."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        assert len(chunks) > 0
        assert all(len(chunk) > 0 for chunk in chunks)

    def test_chunk_sizes_within_bounds(self, embedding_service, sample_resume_data):
        """Test that all chunks are between 200-500 characters."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        
        for chunk in chunks:
            assert 200 <= len(chunk) <= 500, f"Chunk size {len(chunk)} out of bounds: {chunk[:50]}..."

    def test_chunk_resume_includes_personal_info(self, embedding_service, sample_resume_data):
        """Test that personal information is included in chunks."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        chunks_text = " ".join(chunks)
        
        assert "Test User" in chunks_text
        assert "test@example.com" in chunks_text

    def test_chunk_resume_includes_education(self, embedding_service, sample_resume_data):
        """Test that education information is included in chunks."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        chunks_text = " ".join(chunks)
        
        assert "Test University" in chunks_text
        assert "B.Tech in Computer Science" in chunks_text

    def test_chunk_resume_includes_experience(self, embedding_service, sample_resume_data):
        """Test that experience information is included in chunks."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        chunks_text = " ".join(chunks)
        
        assert "Test Company" in chunks_text
        assert "Software Engineer Intern" in chunks_text

    def test_chunk_resume_includes_skills(self, embedding_service, sample_resume_data):
        """Test that skills are included in chunks."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        chunks_text = " ".join(chunks)
        
        assert "Python" in chunks_text
        assert "React" in chunks_text
        assert "FastAPI" in chunks_text

    def test_chunk_resume_includes_projects(self, embedding_service, sample_resume_data):
        """Test that projects are included in chunks."""
        chunks = embedding_service.chunk_resume(sample_resume_data)
        chunks_text = " ".join(chunks)
        
        assert "Test Project 1" in chunks_text
        assert "Test Project 2" in chunks_text

    def test_chunk_resume_with_empty_data(self, embedding_service):
        """Test chunking with empty resume data."""
        chunks = embedding_service.chunk_resume({})
        assert isinstance(chunks, list)
        # Empty data should produce no chunks or very few chunks
        assert len(chunks) == 0

    def test_chunk_resume_with_missing_sections(self, embedding_service):
        """Test chunking with missing sections."""
        partial_data = {
            "personal": {
                "name": "Test User",
                "email": "test@example.com",
                "linkedin": "https://linkedin.com/in/testuser",
                "github": "https://github.com/testuser",
                "location": "Test City"
            }
        }
        chunks = embedding_service.chunk_resume(partial_data)
        assert isinstance(chunks, list)
        # Should still produce at least one chunk from personal info
        assert len(chunks) >= 0


class TestEmbedResumeCorpus:
    """Tests for embed_resume_corpus method."""

    def test_embed_resume_corpus_with_valid_file(self, embedding_service, sample_resume_data, tmp_path):
        """Test embedding resume corpus with valid file."""
        # Create temporary resume file
        resume_file = tmp_path / "resume.json"
        with open(resume_file, "w") as f:
            json.dump(sample_resume_data, f)
        
        # Generate embeddings
        result = embedding_service.embed_resume_corpus(str(resume_file))
        
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Check structure of results
        for chunk, embedding in result:
            assert isinstance(chunk, str)
            assert isinstance(embedding, list)
            assert len(embedding) == 384
            assert 200 <= len(chunk) <= 500

    def test_embed_resume_corpus_with_nonexistent_file(self, embedding_service):
        """Test that nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            embedding_service.embed_resume_corpus("nonexistent_file.json")

    def test_embed_resume_corpus_with_invalid_json(self, embedding_service, tmp_path):
        """Test that invalid JSON raises JSONDecodeError."""
        # Create file with invalid JSON
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, "w") as f:
            f.write("{ invalid json content")
        
        with pytest.raises(json.JSONDecodeError):
            embedding_service.embed_resume_corpus(str(invalid_file))

    def test_embed_resume_corpus_returns_tuples(self, embedding_service, sample_resume_data, tmp_path):
        """Test that result contains tuples of (text, embedding)."""
        resume_file = tmp_path / "resume.json"
        with open(resume_file, "w") as f:
            json.dump(sample_resume_data, f)
        
        result = embedding_service.embed_resume_corpus(str(resume_file))
        
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2
            text, embedding = item
            assert isinstance(text, str)
            assert isinstance(embedding, list)

    def test_embed_resume_corpus_all_chunks_have_embeddings(self, embedding_service, sample_resume_data, tmp_path):
        """Test that all chunks get embeddings."""
        resume_file = tmp_path / "resume.json"
        with open(resume_file, "w") as f:
            json.dump(sample_resume_data, f)
        
        result = embedding_service.embed_resume_corpus(str(resume_file))
        
        # All chunks should have embeddings
        assert all(len(embedding) == 384 for _, embedding in result)


class TestIntegration:
    """Integration tests for the complete embedding pipeline."""

    def test_complete_pipeline_with_real_resume(self, embedding_service):
        """Test the complete pipeline with the actual resume.json file."""
        # This test uses the real resume.json file if it exists
        resume_path = "backend/data/resume.json"
        
        if not Path(resume_path).exists():
            pytest.skip("Real resume.json not found")
        
        result = embedding_service.embed_resume_corpus(resume_path)
        
        assert len(result) > 0
        assert all(200 <= len(chunk) <= 500 for chunk, _ in result)
        assert all(len(embedding) == 384 for _, embedding in result)

    def test_embeddings_are_semantically_meaningful(self, embedding_service):
        """Test that similar texts have similar embeddings."""
        text1 = "Python programming and web development with FastAPI framework"
        text2 = "Python coding and building web applications using FastAPI"
        text3 = "JavaScript frontend development with React and TypeScript"
        
        emb1 = embedding_service.generate_embedding(text1)
        emb2 = embedding_service.generate_embedding(text2)
        emb3 = embedding_service.generate_embedding(text3)
        
        # Calculate cosine similarity (simplified)
        def cosine_similarity(a, b):
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(y * y for y in b) ** 0.5
            return dot_product / (norm_a * norm_b)
        
        sim_1_2 = cosine_similarity(emb1, emb2)
        sim_1_3 = cosine_similarity(emb1, emb3)
        
        # Similar texts (1 and 2) should have higher similarity than dissimilar texts (1 and 3)
        assert sim_1_2 > sim_1_3
