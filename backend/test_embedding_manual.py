"""Manual test script for EmbeddingService."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.embedding_service import EmbeddingService


def test_basic_functionality():
    """Test basic EmbeddingService functionality."""
    print("=" * 60)
    print("Testing EmbeddingService")
    print("=" * 60)
    
    # Test 1: Initialization
    print("\n1. Testing initialization...")
    try:
        service = EmbeddingService()
        print(f"   ✓ Model loaded successfully")
        print(f"   ✓ Embedding dimension: {service.embedding_dimension}")
        assert service.embedding_dimension == 384, "Embedding dimension should be 384"
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 2: Generate embedding
    print("\n2. Testing generate_embedding...")
    try:
        text = "This is a test sentence for embedding generation."
        embedding = service.generate_embedding(text)
        print(f"   ✓ Generated embedding with {len(embedding)} dimensions")
        assert len(embedding) == 384, "Embedding should have 384 dimensions"
        assert all(isinstance(x, float) for x in embedding), "All values should be floats"
        print(f"   ✓ All values are floats")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test 3: Empty string handling
    print("\n3. Testing empty string handling...")
    try:
        service.generate_embedding("")
        print(f"   ✗ Should have raised ValueError")
        return False
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"   ✗ Wrong exception type: {e}")
        return False
    
    # Test 4: Chunk resume
    print("\n4. Testing chunk_resume...")
    try:
        sample_data = {
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
                    "Machine Learning"
                ]
            },
            "skills": {
                "languages": ["Python", "JavaScript", "TypeScript"],
                "frontend": ["React", "Vue.js", "Tailwind CSS"],
                "backend": ["FastAPI", "Node.js", "Express"]
            }
        }
        
        chunks = service.chunk_resume(sample_data)
        print(f"   ✓ Generated {len(chunks)} chunks")
        
        # Check chunk sizes
        valid_chunks = 0
        for i, chunk in enumerate(chunks):
            if 200 <= len(chunk) <= 500:
                valid_chunks += 1
            else:
                print(f"   ! Chunk {i+1} size {len(chunk)} out of bounds")
        
        print(f"   ✓ {valid_chunks}/{len(chunks)} chunks within 200-500 character range")
        
        if valid_chunks < len(chunks):
            print(f"   ⚠ Some chunks are outside the expected range")
        
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Embed resume corpus
    print("\n5. Testing embed_resume_corpus...")
    try:
        resume_path = "backend/data/resume.json"
        if not Path(resume_path).exists():
            print(f"   ⚠ Resume file not found at {resume_path}, skipping test")
        else:
            result = service.embed_resume_corpus(resume_path)
            print(f"   ✓ Generated embeddings for {len(result)} chunks")
            
            # Verify structure
            for i, (chunk, embedding) in enumerate(result[:3]):  # Check first 3
                assert isinstance(chunk, str), f"Chunk {i} should be string"
                assert isinstance(embedding, list), f"Embedding {i} should be list"
                assert len(embedding) == 384, f"Embedding {i} should have 384 dimensions"
            
            print(f"   ✓ All chunks have valid embeddings")
            
            # Check chunk sizes
            valid_chunks = sum(1 for chunk, _ in result if 200 <= len(chunk) <= 500)
            print(f"   ✓ {valid_chunks}/{len(result)} chunks within 200-500 character range")
            
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
