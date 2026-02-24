"""Vector store service using ChromaDB for semantic similarity search."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Wrapper for ChromaDB vector store with persistent storage.
    
    This service provides a simple interface for storing document embeddings
    and performing similarity searches. It uses ChromaDB with persistent storage
    for production deployment.
    """

    def __init__(
        self,
        persist_directory: str = "/app/chroma_data",
        collection_name: str = "resume_chunks"
    ):
        """Initialize ChromaDB client with persistent storage.
        
        Args:
            persist_directory: Directory path for persistent storage.
                             Defaults to /app/chroma_data for production.
            collection_name: Name of the collection to store embeddings.
                           Defaults to "resume_chunks".
        
        Raises:
            Exception: If ChromaDB client initialization fails.
        """
        try:
            # Create persist directory if it doesn't exist
            persist_path = Path(persist_directory)
            persist_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Initializing ChromaDB with persist directory: {persist_directory}")
            
            # Initialize ChromaDB client with persistent storage
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            self.collection_name = collection_name
            self.collection = None
            
            logger.info(f"ChromaDB client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB client: {e}")
            raise

    def add_documents(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]] = None
    ) -> None:
        """Store document texts with their embeddings in the vector store.
        
        This method creates or gets the collection and adds documents with their
        embeddings. If the collection already exists, it will be reused.
        
        Args:
            texts: List of text chunks to store.
            embeddings: List of embedding vectors (384-dimensional).
            metadatas: Optional list of metadata dictionaries for each document.
                      If None, empty metadata will be used.
        
        Raises:
            ValueError: If texts and embeddings have different lengths.
            ValueError: If embeddings have incorrect dimensions.
            Exception: If document insertion fails.
        """
        if len(texts) != len(embeddings):
            raise ValueError(
                f"Number of texts ({len(texts)}) must match number of embeddings ({len(embeddings)})"
            )
        
        if metadatas is not None and len(metadatas) != len(texts):
            raise ValueError(
                f"Number of metadatas ({len(metadatas)}) must match number of texts ({len(texts)})"
            )
        
        # Validate embedding dimensions
        if embeddings and len(embeddings[0]) != 384:
            raise ValueError(
                f"Embeddings must be 384-dimensional, got {len(embeddings[0])}"
            )
        
        try:
            # Get or create collection
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                logger.info(f"Using existing collection: {self.collection_name}")
            except Exception:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={
                        "description": "Resume content embeddings for RAG",
                        "embedding_model": "all-MiniLM-L6-v2",
                        "embedding_dimension": 384
                    }
                )
                logger.info(f"Created new collection: {self.collection_name}")
            
            # Prepare metadata (ChromaDB requires non-empty metadata)
            if metadatas is None:
                metadatas = [{"index": i} for i, _ in enumerate(texts)]
            
            # Generate IDs for documents
            ids = [f"doc_{i}" for i in range(len(texts))]
            
            # Add documents to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Successfully added {len(texts)} documents to collection")
            
        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {e}")
            raise

    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 3
    ) -> List[Tuple[str, float]]:
        """Find the k most similar documents to the query embedding.
        
        Performs cosine similarity search and returns the top-k most similar
        documents with their similarity scores.
        
        Args:
            query_embedding: Query embedding vector (384-dimensional).
            k: Number of results to return. Defaults to 3.
        
        Returns:
            List of tuples containing (text_chunk, similarity_score).
            Results are ordered by similarity score in descending order.
            Returns empty list if collection is empty or doesn't exist.
        
        Raises:
            ValueError: If query_embedding has incorrect dimensions.
            ValueError: If k is less than 1.
            Exception: If similarity search fails.
        """
        if len(query_embedding) != 384:
            raise ValueError(
                f"Query embedding must be 384-dimensional, got {len(query_embedding)}"
            )
        
        if k < 1:
            raise ValueError(f"k must be at least 1, got {k}")
        
        try:
            # Get collection if not already loaded
            if self.collection is None:
                try:
                    self.collection = self.client.get_collection(name=self.collection_name)
                except Exception:
                    logger.warning(f"Collection {self.collection_name} does not exist")
                    return []
            
            # Check if collection is empty
            count = self.collection.count()
            if count == 0:
                logger.warning("Collection is empty, returning no results")
                return []
            
            # Perform similarity search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k, count)  # Don't request more than available
            )
            
            # Extract documents and distances
            documents = results.get("documents", [[]])[0]
            distances = results.get("distances", [[]])[0]
            
            # ChromaDB returns distances (lower is better), convert to similarity scores
            # For cosine distance: similarity = 1 - distance
            similarity_scores = [1 - dist for dist in distances]
            
            # Combine documents with scores
            results_with_scores = list(zip(documents, similarity_scores))
            
            logger.info(f"Found {len(results_with_scores)} similar documents")
            
            return results_with_scores
            
        except Exception as e:
            logger.error(f"Failed to perform similarity search: {e}")
            raise

    def clear_collection(self) -> None:
        """Clear all documents from the collection.
        
        This is useful for testing or when re-indexing the resume data.
        
        Raises:
            Exception: If collection deletion fails.
        """
        try:
            if self.collection is not None:
                self.client.delete_collection(name=self.collection_name)
                self.collection = None
                logger.info(f"Cleared collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise

    def get_collection_count(self) -> int:
        """Get the number of documents in the collection.
        
        Returns:
            Number of documents in the collection, or 0 if collection doesn't exist.
        """
        try:
            if self.collection is None:
                try:
                    self.collection = self.client.get_collection(name=self.collection_name)
                except Exception:
                    return 0
            
            return self.collection.count()
        except Exception as e:
            logger.error(f"Failed to get collection count: {e}")
            return 0
