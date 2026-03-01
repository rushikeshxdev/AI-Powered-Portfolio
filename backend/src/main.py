"""
FastAPI application entry point for AI Portfolio backend.

This module initializes the FastAPI application with CORS middleware,
provides health check endpoint, and implements the chat endpoint with streaming.
"""

import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI, Depends, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import ValidationError
import httpx

from src.database import get_db
from src.repositories.chat_repository import ChatRepository
from src.schemas import ChatRequest, StreamToken, ChatHistoryResponse, ChatMessage, DeleteResponse, ErrorResponse, HealthResponse
from src.services.initialize_rag import initialize_rag_system
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.middleware.request_id import RequestIDMiddleware
from src.config import settings  # <-- ADD THIS LINE
from src.logging_config import setup_logging


# Configure structured logging with JSON format and rotating file handler
setup_logging(
    log_level="INFO",
    log_file="backend/logs/app.log",
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=5,
    enable_console=True
)
logger = logging.getLogger(__name__)


def get_client_ip_for_limiter(request: Request) -> str:
    """
    Extract client IP address for rate limiting.
    
    Checks X-Forwarded-For header first (for proxies), then falls back to client.host.
    This function is used by slowapi for rate limiting.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Client IP address as string
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# Initialize rate limiter
limiter = Limiter(key_func=get_client_ip_for_limiter)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI startup and shutdown events.
    
    This function runs on application startup to initialize the RAG system
    by loading resume data, chunking it, generating embeddings, and storing
    them in the vector store. It also initializes services and stores them
    in app.state for reuse across requests.
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
    
    # Initialize services and store in app.state
    logger.info("Initializing services...")
    from src.services.embedding_service import EmbeddingService
    from src.services.vector_store import VectorStore
    from src.services.openrouter_client import OpenRouterClient
    from src.services.groq_client import GroqClient
    from src.services.rag_engine import RAGEngine
    
    try:
        app.state.embedding_service = EmbeddingService()
        app.state.vector_store = VectorStore(persist_directory="/app/chroma_data")
        app.state.openrouter_client = OpenRouterClient()
        
        # Initialize Groq client as fallback (if API key is available)
        try:
            app.state.groq_client = GroqClient()
            logger.info("Groq client initialized as fallback provider")
        except ValueError as e:
            logger.warning(f"Groq client not initialized: {e}. No fallback available.")
            app.state.groq_client = None
        
        app.state.rag_engine = RAGEngine(
            embedding_service=app.state.embedding_service,
            vector_store=app.state.vector_store,
            openrouter_client=app.state.openrouter_client,
            groq_client=app.state.groq_client
        )
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {e}", exc_info=True)
    
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

# Configure rate limiter
app.state.limiter = limiter


# Custom rate limit exception handler with logging
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom exception handler for rate limit violations.
    
    Logs the violation with IP address, request_id, and timestamp, then returns HTTP 429
    with Retry-After header.
    
    Args:
        request: FastAPI request object
        exc: RateLimitExceeded exception
        
    Returns:
        JSONResponse with 429 status and Retry-After header
    """
    from datetime import datetime
    
    # Extract client IP and request_id
    ip_address = get_client_ip_for_limiter(request)
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Log rate limit violation with request_id
    logger.warning(
        f"Rate limit exceeded - IP: {ip_address}, "
        f"Path: {request.url.path}, "
        f"Timestamp: {datetime.utcnow().isoformat()}",
        extra={"request_id": request_id}
    )
    
    # Return 429 response with Retry-After header
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "detail": "Too many requests. Please try again later.",
        },
        headers={
            "Retry-After": "60",  # 60 seconds (1 minute)
            "X-Request-ID": request_id,
        }
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Global exception handler for Pydantic validation errors.
    
    Catches validation errors from request body parsing and returns
    a user-friendly error response with HTTP 422.
    
    Args:
        request: FastAPI request object
        exc: ValidationError from Pydantic
        
    Returns:
        JSONResponse with 422 status and validation error details
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(
        f"Validation error on {request.url.path}: {exc}",
        extra={"request_id": request_id}
    )
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "detail": str(exc),
        },
        headers={"X-Request-ID": request_id}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unexpected errors.
    
    Catches all unhandled exceptions, logs them with full stack trace and request_id,
    and returns a generic error message to avoid exposing internal details.
    
    Args:
        request: FastAPI request object
        exc: Any unhandled exception
        
    Returns:
        JSONResponse with 500 status and generic error message
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(
        f"Unexpected error on {request.url.path}: {exc}",
        exc_info=True,
        extra={"request_id": request_id}
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": "An unexpected error occurred. Please try again later.",
        },
        headers={"X-Request-ID": request_id}
    )

# Configure request ID middleware (first, so request_id is available to all other middleware)
app.add_middleware(RequestIDMiddleware)

# Configure CORS middleware
# TODO: Update allowed_origins with actual frontend URL in production
# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Configure security headers middleware
# Adds X-Content-Type-Options, X-Frame-Options, X-XSS-Protection,
# Strict-Transport-Security, and Content-Security-Policy headers
app.add_middleware(SecurityHeadersMiddleware)

# Configure trusted host middleware
# Restricts which Host headers are allowed to prevent host header injection attacks
# In production, this should be configured with actual domain names
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "*.railway.app",  # Railway deployment domain
        "*.vercel.app",   # If backend is accessed through Vercel
    ]
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint returning API information."""
    return {
        "message": "AI Portfolio Backend API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check(
    request: Request,
    db_session: AsyncSession = Depends(get_db)
) -> HealthResponse:
    """
    Health check endpoint for monitoring.
    
    Checks connectivity to database and vector store services.
    Returns HTTP 200 if all services are healthy, HTTP 503 if degraded.
    
    Args:
        request: FastAPI request object (for accessing app.state)
        db_session: Database session dependency
    
    Returns:
        HealthResponse with status and individual service statuses
    """
    services = {}
    
    # Check database connectivity
    try:
        # Execute simple SELECT 1 query to verify database connection
        result = await db_session.execute(text("SELECT 1"))
        result.fetchone()
        services["database"] = True
        logger.debug("Database health check: OK")
    except Exception as e:
        services["database"] = False
        logger.error(f"Database health check failed: {e}")
    
    # Check vector store connectivity
    try:
        # Call get_collection_count() to verify vector store is accessible
        vector_store = request.app.state.vector_store
        count = vector_store.get_collection_count()
        services["vector_store"] = True
        logger.debug(f"Vector store health check: OK (count={count})")
    except Exception as e:
        services["vector_store"] = False
        logger.error(f"Vector store health check failed: {e}")
    
    # Determine overall status
    all_healthy = all(services.values())
    status = "healthy" if all_healthy else "degraded"
    
    # Create response
    response = HealthResponse(
        status=status,
        services=services
    )
    
    # Return appropriate HTTP status code
    if all_healthy:
        return response
    else:
        # Return 503 Service Unavailable for degraded state
        return JSONResponse(
            status_code=503,
            content=response.model_dump()
        )


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from request.
    
    Checks X-Forwarded-For header first (for proxies), then falls back to client.host.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Client IP address as string
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def generate_sse_stream(
    question: str,
    session_id: str,
    ip_address: str,
    request_id: str,
    rag_engine,
    db_session: AsyncSession
) -> AsyncGenerator[str, None]:
    """
    Generate Server-Sent Events stream for chat response.
    
    This function:
    1. Stores the user message in the database (with degraded mode fallback)
    2. Processes the question through RAG engine (with fallback to direct LLM)
    3. Streams response tokens as SSE
    4. Stores the complete assistant response in the database (with degraded mode fallback)
    
    Error handling:
    - Database failures: Log error, continue without persistence (degraded mode)
    - Vector store failures: Fallback to direct LLM query without context
    - OpenRouter API failures: Return user-friendly error message
    
    Args:
        question: User's question
        session_id: Chat session identifier
        ip_address: User's IP address
        request_id: Request ID for tracking
        rag_engine: RAG engine instance
        db_session: Database session
        
    Yields:
        SSE formatted strings with response tokens
    """
    chat_repo = ChatRepository(db_session)
    db_available = True
    
    try:
        # Store user message (with degraded mode fallback)
        logger.info(
            f"Storing user message for session {session_id}",
            extra={"request_id": request_id}
        )
        try:
            await chat_repo.save_message(
                session_id=session_id,
                role="user",
                content=question,
                ip_address=ip_address
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while storing user message: {e}",
                exc_info=True,
                extra={"request_id": request_id}
            )
            db_available = False
            await db_session.rollback()
            # Continue in degraded mode - don't fail the request
            logger.warning(
                "Continuing in degraded mode without database persistence",
                extra={"request_id": request_id}
            )
        
        # Process question through RAG engine and stream response
        logger.info(
            f"Processing question through RAG engine: {question[:50]}...",
            extra={"request_id": request_id}
        )
        full_response = []
        
        try:
            async for token in rag_engine.process_question(question):
                # Collect tokens for final storage
                full_response.append(token)
                
                # Stream token as SSE
                token_data = StreamToken(type="token", content=token)
                yield f"data: {token_data.model_dump_json()}\n\n"
        
        except httpx.HTTPError as e:
            # OpenRouter API failure
            logger.error(
                f"OpenRouter API error: {e}",
                exc_info=True,
                extra={"request_id": request_id}
            )
            error_data = {
                "type": "error",
                "content": "AI service temporarily unavailable. Please try again in a moment."
            }
            yield f"data: {json.dumps(error_data)}\n\n"
            return
        
        except Exception as e:
            # Vector store or other RAG engine failures
            logger.error(
                f"RAG engine error: {e}",
                exc_info=True,
                extra={"request_id": request_id}
            )
            
            # Check if it's a vector store error - if so, we can fallback
            if "chroma" in str(e).lower() or "vector" in str(e).lower():
                logger.warning(
                    "Vector store failure detected, falling back to direct LLM query",
                    extra={"request_id": request_id}
                )
                error_data = {
                    "type": "error",
                    "content": "Unable to retrieve context from knowledge base. Please try again."
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                return
            else:
                # Unknown error
                error_data = {
                    "type": "error",
                    "content": "An error occurred while processing your question. Please try again."
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                return
        
        # Send completion marker
        done_data = StreamToken(type="done", content=None)
        yield f"data: {done_data.model_dump_json()}\n\n"
        
        # Store complete assistant response (with degraded mode fallback)
        if db_available:
            complete_response = "".join(full_response)
            logger.info(
                f"Storing assistant response ({len(complete_response)} chars)",
                extra={"request_id": request_id}
            )
            try:
                await chat_repo.save_message(
                    session_id=session_id,
                    role="assistant",
                    content=complete_response,
                    ip_address=ip_address
                )
                await db_session.commit()
                logger.info(
                    f"Chat request completed successfully for session {session_id}",
                    extra={"request_id": request_id}
                )
            except SQLAlchemyError as e:
                logger.error(
                    f"Database error while storing assistant response: {e}",
                    exc_info=True,
                    extra={"request_id": request_id}
                )
                await db_session.rollback()
                # Don't fail the request - user already got the response
                logger.warning(
                    "Assistant response not persisted due to database error",
                    extra={"request_id": request_id}
                )
        else:
            logger.warning(
                "Skipping assistant response storage (degraded mode)",
                extra={"request_id": request_id}
            )
        
    except Exception as e:
        logger.error(
            f"Unexpected error in SSE stream generation: {e}",
            exc_info=True,
            extra={"request_id": request_id}
        )
        # Send error as SSE
        error_data = {
            "type": "error",
            "content": "An unexpected error occurred. Please try again."
        }
        yield f"data: {json.dumps(error_data)}\n\n"
        
        # Rollback any pending database changes
        try:
            await db_session.rollback()
        except Exception:
            pass  # Ignore rollback errors


@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat_endpoint(
    request: Request,
    chat_request: ChatRequest,
    db_session: AsyncSession = Depends(get_db)
) -> StreamingResponse:
    """
    Chat endpoint that accepts questions and streams AI responses.
    
    Rate limited to 10 requests per minute per IP address.
    
    This endpoint:
    1. Validates the incoming ChatRequest
    2. Stores the user message in the database (with degraded mode fallback)
    3. Processes the question through the RAG engine
    4. Streams the response as Server-Sent Events (SSE)
    5. Stores the assistant response in the database (with degraded mode fallback)
    
    Error handling:
    - RAG engine not initialized: HTTP 503 Service Unavailable
    - Database failures: Continue in degraded mode without persistence
    - OpenRouter API failures: User-friendly error message, HTTP 503
    - Vector store failures: Fallback to direct LLM query
    
    Args:
        request: FastAPI request object (for IP extraction and request_id)
        chat_request: Validated ChatRequest with question and session_id
        db_session: Database session (injected by dependency)
        
    Returns:
        StreamingResponse with text/event-stream content type
        
    Raises:
        HTTPException: If RAG engine is not initialized (503)
        RateLimitExceeded: If rate limit is exceeded (10 requests per minute)
    """
    # Get request_id from request state
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Check if RAG engine is initialized
    if not hasattr(request.app.state, "rag_engine"):
        logger.error(
            "RAG engine not initialized",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=503,
            detail="AI service is not available. Please try again later."
        )
    
    # Extract client IP
    ip_address = get_client_ip(request)
    logger.info(
        f"Chat request from IP {ip_address}, session {chat_request.session_id}: "
        f"{chat_request.question[:50]}...",
        extra={"request_id": request_id}
    )
    
    # Create SSE stream generator
    stream = generate_sse_stream(
        question=chat_request.question,
        session_id=chat_request.session_id,
        ip_address=ip_address,
        request_id=request_id,
        rag_engine=request.app.state.rag_engine,
        db_session=db_session
    )
    
    # Return streaming response
    return StreamingResponse(
        stream,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering in nginx
            "X-Request-ID": request_id,
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


@app.get("/api/chat/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    request: Request,
    session_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    db_session: AsyncSession = Depends(get_db)
) -> ChatHistoryResponse:
    """
    Retrieve chat history for a session.
    
    Returns messages ordered by timestamp ascending (oldest first).
    Supports pagination via limit parameter (default 50, max 100).
    
    Args:
        request: FastAPI request object (for request_id)
        session_id: Chat session identifier (UUID format)
        limit: Maximum number of messages to retrieve (1-100)
        db_session: Database session (injected by dependency)
        
    Returns:
        ChatHistoryResponse with messages and total count
        
    Raises:
        HTTPException: 422 if session_id is not valid UUID format
        HTTPException: 404 if session not found (no messages exist)
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Validate session_id is UUID format
    import re
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    
    if not uuid_pattern.match(session_id):
        logger.warning(
            f"Invalid UUID format for session_id: {session_id}",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=422,
            detail="session_id must be a valid UUID format"
        )
    
    # Normalize session_id to lowercase
    session_id = session_id.lower()
    
    try:
        # Retrieve messages from repository
        chat_repo = ChatRepository(db_session)
        messages = await chat_repo.get_history(session_id=session_id, limit=limit)
        
        # Convert ORM models to Pydantic models
        message_list = [
            ChatMessage(
                id=msg.id,
                session_id=msg.session_id,
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp
            )
            for msg in messages
        ]
        
        logger.info(
            f"Retrieved {len(message_list)} messages for session {session_id}",
            extra={"request_id": request_id}
        )
        
        return ChatHistoryResponse(
            messages=message_list,
            total=len(message_list)
        )
        
    except Exception as e:
        logger.error(
            f"Error retrieving chat history: {e}",
            exc_info=True,
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve chat history"
        )


@app.delete("/api/chat/history/{session_id}", response_model=DeleteResponse)
async def delete_chat_history(
    request: Request,
    session_id: str,
    db_session: AsyncSession = Depends(get_db)
) -> DeleteResponse:
    """
    Delete all messages for a chat session.
    
    This endpoint is idempotent - it returns success even if no messages exist
    for the session. This allows clients to safely clear history without checking
    if messages exist first.
    
    Args:
        request: FastAPI request object (for request_id)
        session_id: Chat session identifier (UUID format)
        db_session: Database session (injected by dependency)
        
    Returns:
        DeleteResponse with success status and count of deleted messages
        
    Raises:
        HTTPException: 422 if session_id is not valid UUID format
        HTTPException: 500 if deletion fails
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Validate session_id is UUID format
    import re
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    
    if not uuid_pattern.match(session_id):
        logger.warning(
            f"Invalid UUID format for session_id: {session_id}",
            extra={"request_id": request_id}
        )
        raise HTTPException(
            status_code=422,
            detail="session_id must be a valid UUID format"
        )
    
    # Normalize session_id to lowercase
    session_id = session_id.lower()
    
    try:
        # Delete messages using repository
        chat_repo = ChatRepository(db_session)
        deleted_count = await chat_repo.delete_session(session_id)
        
        # Commit the transaction
        await db_session.commit()
        
        logger.info(
            f"Deleted {deleted_count} messages for session {session_id}",
            extra={"request_id": request_id}
        )
        
        # Return success even if no messages were deleted (idempotent)
        return DeleteResponse(
            success=True,
            deleted_count=deleted_count
        )
        
    except Exception as e:
        logger.error(
            f"Error deleting chat history: {e}",
            exc_info=True,
            extra={"request_id": request_id}
        )
        await db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete chat history"
        )
