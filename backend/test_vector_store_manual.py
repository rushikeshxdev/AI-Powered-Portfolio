"""Manual test script for VectorStore to verify functionality."""

import tempfile
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.vector_store import VectorStore


def test_vector_store_basic():
    """Test basic VectorStore functionality."""
    print("Testing VectorStore...")
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Using temporary directory: {tmpdir}")
        
        # Initialize VectorStore
        print("\n1. Initializing VectorStore...")
        vector_store = VectorStore(
            persist_directory=tmpdir,
            collection_name="test_collection"
        )
        print("✓ VectorStore initialized successfully")
        
        # Prepare test data
        texts = [
            "Python is a high-level programming language.",
            "JavaScript is used for web development.",
            "Machine learning is a subset of artificial intelligence.",
        ]
        embeddings = [
            [0.1] * 384,
            [0.2] * 384,
            [0.3] * 384,
        ]
        metadatas = [
            {"section": "skills", "subsection": "languages"},
            {"section": "skills", "subsection": "frontend"},
            {"section": "experience", "subsection": "ai_ml"},
        ]
        
        # Test add_documents
        print("\n2. Adding documents...")
        vector_store.add_documents(texts, embeddings, metadatas)
        count = vector_store.get_collection_count()
        print(f"✓ Added {count} documents successfully")
        assert count == 3, f"Expected 3 documents, got {count}"
        
        # Test similarity_search
        print("\n3. Testing similarity search...")
        query_embedding = [0.15] * 384  # Close to first embedding
        results = vector_store.similarity_search(query_embedding, k=2)
        print(f"✓ Found {len(results)} similar documents")
        assert len(results) == 2, f"Expected 2 results, got {len(results)}"
        
        # Verify results structure
        for i, (text, score) in enumerate(results):
            print(f"  Result {i+1}: score={score:.4f}, text='{text[:50]}...'")
            assert isinstance(text, str), "Text should be string"
            assert isinstance(score, float), "Score should be float"
        
        # Verify scores are ordered
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True), "Scores should be in descending order"
        print("✓ Results are properly ordered by similarity")
        
        # Test edge cases
        print("\n4. Testing edge cases...")
        
        # Test with k=1
        results_k1 = vector_store.similarity_search(query_embedding, k=1)
        assert len(results_k1) == 1, "Should return exactly 1 result"
        print("✓ k=1 works correctly")
        
        # Test with k > available documents
        results_k10 = vector_store.similarity_search(query_embedding, k=10)
        assert len(results_k10) == 3, "Should return only available documents"
        print("✓ k > available documents handled correctly")
        
        # Test clear_collection
        print("\n5. Testing clear_collection...")
        vector_store.clear_collection()
        count_after_clear = vector_store.get_collection_count()
        assert count_after_clear == 0, "Collection should be empty after clear"
        print("✓ Collection cleared successfully")
        
        print("\n" + "="*60)
        print("✓ All tests passed successfully!")
        print("="*60)


def test_vector_store_error_handling():
    """Test VectorStore error handling."""
    print("\nTesting error handling...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        vector_store = VectorStore(persist_directory=tmpdir)
        
        # Test mismatched lengths
        print("\n1. Testing mismatched lengths...")
        try:
            vector_store.add_documents(
                texts=["text1", "text2"],
                embeddings=[[0.1] * 384]  # Only one embedding
            )
            print("✗ Should have raised ValueError")
            sys.exit(1)
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test wrong embedding dimension
        print("\n2. Testing wrong embedding dimension...")
        try:
            vector_store.add_documents(
                texts=["text1"],
                embeddings=[[0.1] * 128]  # Wrong dimension
            )
            print("✗ Should have raised ValueError")
            sys.exit(1)
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test invalid k
        print("\n3. Testing invalid k...")
        try:
            vector_store.similarity_search([0.1] * 384, k=0)
            print("✗ Should have raised ValueError")
            sys.exit(1)
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        # Test wrong query embedding dimension
        print("\n4. Testing wrong query embedding dimension...")
        try:
            vector_store.similarity_search([0.1] * 128, k=3)
            print("✗ Should have raised ValueError")
            sys.exit(1)
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {e}")
        
        print("\n✓ All error handling tests passed!")


def test_vector_store_persistence():
    """Test VectorStore persistence across instances."""
    print("\nTesting persistence...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create first instance and add documents
        print("\n1. Creating first instance and adding documents...")
        vector_store1 = VectorStore(
            persist_directory=tmpdir,
            collection_name="persist_test"
        )
        texts = ["Document 1", "Document 2", "Document 3"]
        embeddings = [[0.1] * 384, [0.2] * 384, [0.3] * 384]
        vector_store1.add_documents(texts, embeddings)
        print(f"✓ Added {vector_store1.get_collection_count()} documents")
        
        # Create second instance with same directory
        print("\n2. Creating second instance with same directory...")
        vector_store2 = VectorStore(
            persist_directory=tmpdir,
            collection_name="persist_test"
        )
        
        # Search in second instance
        results = vector_store2.similarity_search([0.1] * 384, k=3)
        print(f"✓ Found {len(results)} documents in second instance")
        assert len(results) == 3, "Should find all documents from first instance"
        
        print("\n✓ Persistence test passed!")


if __name__ == "__main__":
    try:
        test_vector_store_basic()
        test_vector_store_error_handling()
        test_vector_store_persistence()
        
        print("\n" + "="*60)
        print("✓✓✓ ALL TESTS PASSED SUCCESSFULLY! ✓✓✓")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
