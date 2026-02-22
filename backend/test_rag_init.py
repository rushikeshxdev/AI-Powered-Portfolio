"""Manual test script for RAG initialization.

This script tests the resume chunking and embedding initialization
to verify that the implementation works correctly.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.initialize_rag import initialize_rag_system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_initialization():
    """Test the RAG initialization process."""
    logger.info("=" * 60)
    logger.info("Testing RAG Initialization")
    logger.info("=" * 60)
    
    try:
        # Test initialization
        result = await initialize_rag_system(
            resume_path="backend/data/resume.json",
            persist_directory="./test_chroma_data",
            force_reinit=True  # Force reinit for testing
        )
        
        logger.info("\nInitialization Result:")
        logger.info(f"  Success: {result['success']}")
        logger.info(f"  Message: {result['message']}")
        logger.info(f"  Chunks Processed: {result.get('chunks_processed', 0)}")
        logger.info(f"  Embeddings Generated: {result.get('embeddings_generated', 0)}")
        logger.info(f"  Documents Stored: {result.get('documents_stored', 0)}")
        
        if result['success']:
            logger.info("\n✓ RAG initialization test PASSED")
            
            # Test idempotency - run again without force_reinit
            logger.info("\nTesting idempotency (should skip initialization)...")
            result2 = await initialize_rag_system(
                resume_path="backend/data/resume.json",
                persist_directory="./test_chroma_data",
                force_reinit=False
            )
            
            logger.info(f"  Message: {result2['message']}")
            logger.info(f"  Existing Documents: {result2.get('existing_documents', 0)}")
            
            if result2.get('existing_documents', 0) > 0:
                logger.info("\n✓ Idempotency test PASSED")
            else:
                logger.error("\n✗ Idempotency test FAILED")
        else:
            logger.error("\n✗ RAG initialization test FAILED")
            
    except Exception as e:
        logger.error(f"\n✗ Test failed with exception: {e}", exc_info=True)
    
    logger.info("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_initialization())
