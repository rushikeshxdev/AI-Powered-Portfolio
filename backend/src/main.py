"""
FastAPI application entry point for AI Portfolio backend.

This module initializes the FastAPI application with CORS middleware
and provides basic health check endpoint.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from src.services.initialize_rag import initialize_rag_system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI startup and shutdown events.
    
    This function runs on application startup to initialize the RAG system
    by loading resume data, chunking it, generating embeddings, and storing
    them in the vector store.
    """
    # Startup: Initialize RAG system
    logger.info("Application startup: Initializing RAG system")
    try:
        result = await initialize_rag_system(
            resume_path="backend/data/resume.json",
            persist_directory="/app/chroma_data",
            force_reinit=False  # Only initialize if not already done
        )
        
        if result["success"]:
            logger.info(
                f"RAG system initialized successfully: {result['message']}"
            )
            if result.get("chunks_processed", 0) > 0:
                logger.info(
                    f"Processed {result['chunks_processed']} chunks, "
                    f"generated {result['embeddings_generated']} embeddings"
                )
        else:
            logger.error(f"RAG system initialization failed: {result['message']}")
            # Don't prevent app startup, but log the error
            
    except Exception as e:
        logger.error(f"Error during RAG initialization: {e}", exc_info=True)
        # Don't prevent app startup even if RAG init fails
    
    yield
    
    # Shutdown: Cleanup if needed
    logger.info("Application shutdown")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AI Portfolio Backend",
    description="Backend API for AI-powered portfolio with RAG-based chat assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS middleware
# TODO: Update allowed_origins with actual frontend URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint returning API information."""
    return {
        "message": "AI Portfolio Backend API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring.
    
    Returns:
        Dict with status indicating service health
    """
    return {
        "status": "healthy",
        "service": "ai-portfolio-backend",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
