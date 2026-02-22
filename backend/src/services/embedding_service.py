"""Embedding service for generating semantic embeddings using Sentence Transformers."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using Sentence Transformers.
    
    This service uses the all-MiniLM-L6-v2 model to generate 384-dimensional
    embeddings for text chunks. It handles resume chunking and embedding
    generation for the RAG system.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding service with a Sentence Transformer model.
        
        Args:
            model_name: Name of the Sentence Transformer model to use.
                       Defaults to "all-MiniLM-L6-v2" which produces 384-dimensional vectors.
        
        Raises:
            Exception: If model fails to load.
        """
        try:
            logger.info(f"Loading Sentence Transformer model: {model_name}")
            self.model = SentenceTransformer(model_name)
            self.embedding_dimension = self.model.get_sentence_embedding_dimension()
            logger.info(
                f"Model loaded successfully. Embedding dimension: {self.embedding_dimension}"
            )
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate a 384-dimensional embedding vector for the given text.
        
        Args:
            text: Input text to generate embedding for.
        
        Returns:
            List of 384 float values representing the embedding vector.
        
        Raises:
            ValueError: If text is empty.
            Exception: If embedding generation fails.
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            # Generate embedding and convert to list
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    def chunk_resume(self, resume_data: Dict[str, Any]) -> List[str]:
        """Chunk resume data into meaningful text segments of 200-500 characters.
        
        The chunking strategy preserves context and creates logical segments:
        - Personal info as single chunk
        - Education as single chunk
        - Each experience entry chunked by responsibilities
        - Skills chunked by category
        - Each project chunked into overview and details
        
        Args:
            resume_data: Dictionary containing resume sections (personal, education,
                        experience, skills, projects).
        
        Returns:
            List of text chunks, each between 200-500 characters.
        """
        chunks = []

        # Personal information chunk
        if "personal" in resume_data:
            personal = resume_data["personal"]
            chunk = (
                f"{personal.get('name', '')} is located in {personal.get('location', '')}. "
                f"Contact: {personal.get('email', '')}, "
                f"LinkedIn: {personal.get('linkedin', '')}, "
                f"GitHub: {personal.get('github', '')}"
            )
            if len(chunk) >= 200:
                chunks.append(chunk)

        # Education chunk
        if "education" in resume_data:
            edu = resume_data["education"]
            coursework = ", ".join(edu.get("relevant_coursework", []))
            chunk = (
                f"Education: {edu.get('degree', '')} from {edu.get('institution', '')}, "
                f"CGPA: {edu.get('cgpa', '')}, graduating in {edu.get('expected_graduation', '')}. "
                f"Relevant coursework includes {coursework}."
            )
            if len(chunk) >= 200:
                chunks.append(chunk)

        # Experience chunks
        if "experience" in resume_data:
            for exp in resume_data["experience"]:
                # Main experience chunk
                responsibilities = " ".join(exp.get("responsibilities", []))
                technologies = ", ".join(exp.get("technologies", []))
                chunk = (
                    f"Current role: {exp.get('role', '')} at {exp.get('company', '')} "
                    f"({exp.get('location', '')}). Duration: {exp.get('duration', '')}. "
                    f"Responsibilities: {responsibilities[:300]}"
                )
                if len(chunk) >= 200:
                    chunks.append(chunk)

                # Technologies chunk if needed
                if technologies:
                    tech_chunk = (
                        f"{exp.get('role', '')} at {exp.get('company', '')} uses technologies: {technologies}"
                    )
                    if len(tech_chunk) >= 200:
                        chunks.append(tech_chunk)

        # Skills chunks by category
        if "skills" in resume_data:
            skills = resume_data["skills"]
            
            if "languages" in skills:
                chunk = f"Programming Languages: {', '.join(skills['languages'])}"
                if len(chunk) >= 200:
                    chunks.append(chunk)
            
            if "frontend" in skills:
                chunk = f"Frontend Technologies: {', '.join(skills['frontend'])}"
                if len(chunk) >= 200:
                    chunks.append(chunk)
            
            if "backend" in skills:
                chunk = f"Backend Technologies: {', '.join(skills['backend'])}"
                if len(chunk) >= 200:
                    chunks.append(chunk)
            
            if "databases" in skills:
                chunk = f"Database Technologies: {', '.join(skills['databases'])}"
                if len(chunk) >= 200:
                    chunks.append(chunk)
            
            if "devops" in skills:
                chunk = f"DevOps Tools: {', '.join(skills['devops'])}"
                if len(chunk) >= 200:
                    chunks.append(chunk)
            
            if "ai_ml" in skills:
                chunk = f"AI/ML Technologies: {', '.join(skills['ai_ml'])}"
                if len(chunk) >= 200:
                    chunks.append(chunk)

        # Project chunks
        if "projects" in resume_data:
            for project in resume_data["projects"]:
                # Project overview chunk
                technologies = ", ".join(project.get("technologies", []))
                chunk = (
                    f"{project.get('name', '')}: {project.get('description', '')} "
                    f"Technologies: {technologies}"
                )
                if len(chunk) >= 200:
                    chunks.append(chunk[:500])  # Limit to 500 chars

                # Project highlights chunk
                highlights = " ".join(project.get("highlights", []))
                if highlights:
                    highlight_chunk = (
                        f"{project.get('name', '')} highlights: {highlights}"
                    )
                    if len(highlight_chunk) >= 200:
                        chunks.append(highlight_chunk[:500])  # Limit to 500 chars

                # Project links chunk if available
                links = []
                if "github" in project:
                    links.append(f"GitHub: {project['github']}")
                if "demo" in project:
                    links.append(f"Demo: {project['demo']}")
                if links:
                    link_chunk = f"{project.get('name', '')} - {', '.join(links)}"
                    if len(link_chunk) >= 200:
                        chunks.append(link_chunk)

        return chunks

    def embed_resume_corpus(
        self, resume_path: str = "backend/data/resume.json"
    ) -> List[Tuple[str, List[float]]]:
        """Load resume data, chunk it, and generate embeddings for all chunks.
        
        This method orchestrates the complete embedding pipeline:
        1. Load resume.json from the specified path
        2. Chunk the resume into meaningful segments
        3. Generate embeddings for each chunk
        4. Return chunks paired with their embeddings
        
        Args:
            resume_path: Path to the resume.json file. Defaults to backend/data/resume.json.
        
        Returns:
            List of tuples, each containing (text_chunk, embedding_vector).
        
        Raises:
            FileNotFoundError: If resume.json doesn't exist.
            json.JSONDecodeError: If resume.json is invalid.
            Exception: If embedding generation fails.
        """
        # Load resume data
        resume_file = Path(resume_path)
        if not resume_file.exists():
            raise FileNotFoundError(f"Resume file not found: {resume_path}")

        try:
            with open(resume_file, "r", encoding="utf-8") as f:
                resume_data = json.load(f)
            logger.info(f"Loaded resume data from {resume_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in resume file: {e}")
            raise

        # Chunk the resume
        chunks = self.chunk_resume(resume_data)
        logger.info(f"Generated {len(chunks)} chunks from resume")

        # Generate embeddings for all chunks
        embeddings_with_chunks = []
        for i, chunk in enumerate(chunks):
            try:
                embedding = self.generate_embedding(chunk)
                embeddings_with_chunks.append((chunk, embedding))
                logger.debug(f"Generated embedding for chunk {i+1}/{len(chunks)}")
            except Exception as e:
                logger.error(f"Failed to generate embedding for chunk {i+1}: {e}")
                # Continue with other chunks even if one fails
                continue

        logger.info(
            f"Successfully generated {len(embeddings_with_chunks)} embeddings"
        )
        return embeddings_with_chunks
