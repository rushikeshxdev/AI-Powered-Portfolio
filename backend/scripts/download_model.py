# First, remove the corrupted file and create the correct one
cat > backend/scripts/download_model.py << 'ENDOFFILE'
"""Pre-download Sentence Transformer model during build.

This script downloads the Sentence Transformer model during the Render build phase
so it's cached and loads instantly on first request, avoiding the 2+ minute hang.

Usage:
    python scripts/download_model.py
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

def download_model():
    """Download and cache the Sentence Transformer model."""
    print("=" * 60)
    print("Pre-downloading Sentence Transformer Model")
    print("=" * 60)
    print()
    
    try:
        # Set cache directory to persist from build to runtime
        cache_dir = os.path.join(os.getcwd(), '.cache')
        os.environ['SENTENCE_TRANSFORMERS_HOME'] = cache_dir
        os.environ['TRANSFORMERS_CACHE'] = cache_dir
        
        print(f"Cache directory: {cache_dir}")
        
        from sentence_transformers import SentenceTransformer
        
        model_name = "all-MiniLM-L6-v2"
        print(f"Downloading model: {model_name}")
        print("This will take 30-60 seconds and cache the model...")
        print()
        
        # Download and cache the model
        model = SentenceTransformer(model_name, cache_folder=cache_dir)
        
        # Verify it works
        test_embedding = model.encode("test", convert_to_numpy=True)
        embedding_dim = len(test_embedding)
        
        print()
        print("✓ Model downloaded and cached successfully!")
        print(f"✓ Embedding dimension: {embedding_dim}")
        print(f"✓ Cache location: {cache_dir}")
        print(f"✓ Model will now load instantly on first request")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error downloading model: {e}")
        print("Build will continue, but first request will be slow.")
        # Don't fail the build - just warn
        return 0


if __name__ == "__main__":
    sys.exit(download_model())
ENDOFFILE