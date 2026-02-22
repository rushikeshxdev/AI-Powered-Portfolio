"""Resume chunking and embedding initialization script for RAG system.

This module provides functionality to initialize the vector store with resume
embeddings on application startup. It orchestrates the complete pipeline:
1. Load resume.json
2. Chunk into 200-500 character segments
3. Generate embeddings using EmbeddingService
4. Store in VectorStore with metadata

The initialization is idempotent and can be run multiple times safely.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from .embedding_service import EmbeddingService
from .vector_store import VectorStore

logger = logging.getLogger(__name__)


class RAGInitializer:
    """Handles initialization of the RAG system with resume embeddings."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        resume_path: str = "backend/data/resume.json"
    ):
        """Initialize the RAG initializer.
        
        Args:
            embedding_service: Service for generating embeddings.
            vector_store: Vector store for storing embeddings.
            resume_path: Path to resume.json file.
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.resume_path = resume_path

    def _create_metadata(self, chunk: str, index: int) -> Dict[str, Any]:
        """Create metadata for a resume chunk.
        
        Analyzes the chunk content to determine which section it belongs to
        and creates appropriate metadata.
        
        Args:
            chunk: The text chunk.
            index: Index of the chunk in the list.
        
        Returns:
            Dictionary containing metadata about the chunk.
        """
        metadata = {
            "chunk_id": f"chunk_{index}",
            "char_count": len(chunk),
            "source": "resume.json"
        }
        
        # Determine section based on content
        chunk_lower = chunk.lower()
        
        if any(keyword in chunk_lower for keyword in ["contact:", "email:", "linkedin:", "github:"]):
            metadata["section"] = "personal"
            metadata["subsection"] = "contact_info"
        elif "education:" in chunk_lower or "b.tech" in chunk_lower or "cgpa:" in chunk_lower:
            metadata["section"] = "education"
            metadata["subsection"] = "academic_background"
        elif any(keyword in chunk_lower for keyword in ["current role:", "responsibilities:", "duration:"]):
            metadata["section"] = "experience"
            metadata["subsection"] = "work_experience"
        elif any(keyword in chunk_lower for keyword in [
            "programming languages:",
            "frontend technologies:",
            "backend technologies:",
            "database technologies:",
            "devops tools:",
            "ai/ml technologies:"
        ]):
            metadata["section"] = "skills"
            # Determine skill category
            if "programming languages:" in chunk_lower:
                metadata["subsection"] = "languages"
            elif "frontend" in chunk_lower:
                metadata["subsection"] = "frontend"
            elif "backend" in chunk_lower:
                metadata["subsection"] = "backend"
            elif "database" in chunk_lower:
                metadata["subsection"] = "databases"
            elif "devops" in chunk_lower:
                metadata["subsection"] = "devops"
            elif "ai/ml" in chunk_lower:
                metadata["subsection"] = "ai_ml"
        else:
            # Likely a project chunk
            metadata["section"] = "projects"
            # Try to extract project name (usually at the start)
            first_colon = chunk.find(":")
            if first_colon > 0 and first_colon < 100:
                project_name = chunk[:first_colon].strip()
                metadata["subsection"] = f"project_{project_name.lower().replace(' ', '_')}"
            else:
                metadata["subsection"] = f"project_{index}"
        
        return metadata

    async def initialize(self, force_reinit: bool = False) -> Dict[str, Any]:
        """Initialize the vector store with resume embeddings.
        
        This method is idempotent - it checks if the vector store is already
        populated and skips initialization unless force_reinit is True.
        
        Args:
            force_reinit: If True, clear existing data and reinitialize.
                         If False, skip if vector store already has data.
        
        Returns:
            Dictionary containing initialization results:
            - success: bool indicating if initialization succeeded
            - chunks_processed: number of chunks processed
            - embeddings_generated: number of embeddings generated
            - message: status message
        
        Raises:
            FileNotFoundError: If resume.json doesn't exist.
            Exception: If initialization fails.
        """
        try:
            logger.info("Starting RAG system initialization")
            
            # Check if vector store already has data (idempotency check)
            existing_count = self.vector_store.get_collection_count()
            if existing_count > 0 and not force_reinit:
                logger.info(
                    f"Vector store already contains {existing_count} documents. "
                    "Skipping initialization. Use force_reinit=True to reinitialize."
                )
                return {
                    "success": True,
                    "chunks_processed": 0,
                    "embeddings_generated": 0,
                    "existing_documents": existing_count,
                    "message": "Vector store already initialized"
                }
            
            # Clear existing data if force_reinit
            if force_reinit and existing_count > 0:
                logger.info(f"Clearing {existing_count} existing documents")
                self.vector_store.clear_collection()
            
            # Verify resume file exists
            resume_file = Path(self.resume_path)
            if not resume_file.exists():
                error_msg = f"Resume file not found: {self.resume_path}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            # Load resume and generate embeddings
            logger.info(f"Loading resume from {self.resume_path}")
            chunks_with_embeddings = self.embedding_service.embed_resume_corpus(
                self.resume_path
            )
            
            if not chunks_with_embeddings:
                logger.warning("No chunks generated from resume")
                return {
                    "success": False,
                    "chunks_processed": 0,
                    "embeddings_generated": 0,
                    "message": "No chunks generated from resume"
                }
            
            # Separate chunks and embeddings
            chunks = [chunk for chunk, _ in chunks_with_embeddings]
            embeddings = [embedding for _, embedding in chunks_with_embeddings]
            
            # Create metadata for each chunk
            metadatas = [
                self._create_metadata(chunk, i)
                for i, chunk in enumerate(chunks)
            ]
            
            # Store in vector store
            logger.info(f"Storing {len(chunks)} chunks in vector store")
            self.vector_store.add_documents(
                texts=chunks,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            # Verify storage
            final_count = self.vector_store.get_collection_count()
            
            logger.info(
                f"RAG initialization complete. "
                f"Processed {len(chunks)} chunks, "
                f"generated {len(embeddings)} embeddings, "
                f"stored {final_count} documents"
            )
            
            return {
                "success": True,
                "chunks_processed": len(chunks),
                "embeddings_generated": len(embeddings),
                "documents_stored": final_count,
                "message": "RAG system initialized successfully"
            }
            
        except FileNotFoundError as e:
            logger.error(f"Resume file not found: {e}")
            return {
                "success": False,
                "chunks_processed": 0,
                "embeddings_generated": 0,
                "message": f"Resume file not found: {e}"
            }
        except Exception as e:
            logger.error(f"Failed to initialize RAG system: {e}", exc_info=True)
            return {
                "success": False,
                "chunks_processed": 0,
                "embeddings_generated": 0,
                "message": f"Initialization failed: {str(e)}"
            }


async def initialize_rag_system(
    resume_path: str = "backend/data/resume.json",
    persist_directory: str = "/app/chroma_data",
    force_reinit: bool = False
) -> Dict[str, Any]:
    """Convenience function to initialize the RAG system.
    
    This function creates the necessary services and initializes the vector store.
    It's designed to be called during FastAPI startup.
    
    Args:
        resume_path: Path to resume.json file.
        persist_directory: Directory for ChromaDB persistence.
        force_reinit: If True, reinitialize even if data exists.
    
    Returns:
        Dictionary containing initialization results.
    """
    try:
        logger.info("Initializing RAG system services")
        
        # Initialize services
        embedding_service = EmbeddingService()
        vector_store = VectorStore(persist_directory=persist_directory)
        
        # Create initializer and run
        initializer = RAGInitializer(
            embedding_service=embedding_service,
            vector_store=vector_store,
            resume_path=resume_path
        )
        
        result = await initializer.initialize(force_reinit=force_reinit)
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}", exc_info=True)
        return {
            "success": False,
            "chunks_processed": 0,
            "embeddings_generated": 0,
            "message": f"Initialization failed: {str(e)}"
        }
