"""
Verification script for AI provider fallback system.

This script verifies that:
1. Groq client can be initialized
2. Config has groq_api_key field
3. RAG engine accepts both clients
"""

import sys
import os

# Add backend/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def verify_config():
    """Verify config has groq_api_key field."""
    print("1. Verifying config...")
    try:
        from config import settings
        
        # Check if groq_api_key field exists
        assert hasattr(settings, 'groq_api_key'), "groq_api_key field missing"
        print(f"   ✓ Config has groq_api_key field")
        print(f"   ✓ Groq API key present: {bool(settings.groq_api_key)}")
        return True
    except Exception as e:
        print(f"   ✗ Config verification failed: {e}")
        return False

def verify_groq_client():
    """Verify Groq client can be imported and initialized."""
    print("\n2. Verifying Groq client...")
    try:
        from services.groq_client import GroqClient
        print(f"   ✓ GroqClient imported successfully")
        
        # Check if it has the required method
        assert hasattr(GroqClient, 'stream_completion'), "stream_completion method missing"
        print(f"   ✓ GroqClient has stream_completion method")
        return True
    except Exception as e:
        print(f"   ✗ Groq client verification failed: {e}")
        return False

def verify_rag_engine():
    """Verify RAG engine accepts groq_client parameter."""
    print("\n3. Verifying RAG engine...")
    try:
        from services.rag_engine import RAGEngine
        import inspect
        
        # Check __init__ signature
        sig = inspect.signature(RAGEngine.__init__)
        params = list(sig.parameters.keys())
        
        assert 'groq_client' in params, "groq_client parameter missing from __init__"
        print(f"   ✓ RAGEngine accepts groq_client parameter")
        
        # Check if it's optional
        param = sig.parameters['groq_client']
        assert param.default is not inspect.Parameter.empty, "groq_client should be optional"
        print(f"   ✓ groq_client parameter is optional")
        return True
    except Exception as e:
        print(f"   ✗ RAG engine verification failed: {e}")
        return False

def verify_requirements():
    """Verify groq package is in requirements.txt."""
    print("\n4. Verifying requirements.txt...")
    try:
        with open('backend/requirements.txt', 'r') as f:
            content = f.read()
        
        assert 'groq' in content, "groq package not in requirements.txt"
        print(f"   ✓ groq package in requirements.txt")
        return True
    except Exception as e:
        print(f"   ✗ Requirements verification failed: {e}")
        return False

def main():
    """Run all verifications."""
    print("=" * 60)
    print("AI Provider Fallback System Verification")
    print("=" * 60)
    
    results = [
        verify_config(),
        verify_groq_client(),
        verify_rag_engine(),
        verify_requirements()
    ]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All verifications passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some verifications failed")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
