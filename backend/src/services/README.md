# Services Module

This module contains service classes for the AI Portfolio backend.

## Table of Contents

1. [EmbeddingService](#embeddingservice) - Semantic embedding generation
2. [VectorStore](#vectorstore) - ChromaDB vector storage and similarity search

## EmbeddingService

The `EmbeddingService` class provides semantic embedding generation using Sentence Transformers.

### Features

- **Model Initialization**: Loads the `all-MiniLM-L6-v2` model for 384-dimensional embeddings
- **Embedding Generation**: Converts text into semantic vector representations
- **Resume Chunking**: Intelligently splits resume data into 200-500 character chunks
- **Corpus Embedding**: Processes complete resume.json files into embedded chunks

### Usage

```python
from services.embedding_service import EmbeddingService

# Initialize the service
service = EmbeddingService()

# Generate embedding for a single text
text = "Python programming and web development"
embedding = service.generate_embedding(text)
print(f"Embedding dimension: {len(embedding)}")  # 384

# Chunk resume data
resume_data = {
    "personal": {...},
    "education": {...},
    "skills": {...},
    "projects": [...]
}
chunks = service.chunk_resume(resume_data)
print(f"Generated {len(chunks)} chunks")

# Process complete resume file
embeddings = service.embed_resume_corpus("backend/data/resume.json")
for chunk, embedding in embeddings:
    print(f"Chunk: {chunk[:50]}... | Embedding dim: {len(embedding)}")
```

### Methods

#### `__init__(model_name: str = "all-MiniLM-L6-v2")`
Initialize the embedding service with a Sentence Transformer model.

**Parameters:**
- `model_name`: Name of the model to use (default: "all-MiniLM-L6-v2")

**Raises:**
- `Exception`: If model fails to load

#### `generate_embedding(text: str) -> List[float]`
Generate a 384-dimensional embedding vector for the given text.

**Parameters:**
- `text`: Input text to generate embedding for

**Returns:**
- List of 384 float values representing the embedding vector

**Raises:**
- `ValueError`: If text is empty
- `Exception`: If embedding generation fails

#### `chunk_resume(resume_data: Dict[str, Any]) -> List[str]`
Chunk resume data into meaningful text segments of 200-500 characters.

**Chunking Strategy:**
- Personal info as single chunk
- Education as single chunk
- Each experience entry chunked by responsibilities
- Skills chunked by category
- Each project chunked into overview and details

**Parameters:**
- `resume_data`: Dictionary containing resume sections

**Returns:**
- List of text chunks, each between 200-500 characters

#### `embed_resume_corpus(resume_path: str = "backend/data/resume.json") -> List[Tuple[str, List[float]]]`
Load resume data, chunk it, and generate embeddings for all chunks.

**Pipeline:**
1. Load resume.json from the specified path
2. Chunk the resume into meaningful segments
3. Generate embeddings for each chunk
4. Return chunks paired with their embeddings

**Parameters:**
- `resume_path`: Path to the resume.json file

**Returns:**
- List of tuples, each containing (text_chunk, embedding_vector)

**Raises:**
- `FileNotFoundError`: If resume.json doesn't exist
- `json.JSONDecodeError`: If resume.json is invalid
- `Exception`: If embedding generation fails

### Requirements Validation

This implementation validates the following requirements:

- **Requirement 4.1**: Uses Sentence Transformers for embedding generation
- **Requirement 4.2**: Generates embeddings for all resume corpus sections on initialization
- **Requirement 4.4**: Divides resume into logical chunks of 200-500 characters
- **Requirement 4.7**: Uses the same model for both corpus and query embeddings

### Testing

Comprehensive tests are available in `tests/test_embedding_service.py`:

- Initialization tests
- Embedding generation tests (dimension, consistency, error handling)
- Resume chunking tests (size constraints, content completeness)
- Corpus embedding tests (file handling, integration)
- Semantic similarity tests

Run tests with:
```bash
pytest tests/test_embedding_service.py -v
```

### Error Handling

The service includes robust error handling:

- **Model Loading**: Logs and raises exceptions if model fails to load
- **Empty Text**: Raises `ValueError` for empty or whitespace-only input
- **File Not Found**: Raises `FileNotFoundError` for missing resume files
- **Invalid JSON**: Raises `json.JSONDecodeError` for malformed resume data
- **Embedding Failures**: Logs errors and continues processing other chunks

### Logging

The service uses Python's logging module to track:

- Model loading status
- Resume data loading
- Chunk generation count
- Embedding generation progress
- Error conditions

Configure logging in your application:
```python
import logging
logging.basicConfig(level=logging.INFO)
```


---

## VectorStore

The `VectorStore` class provides a wrapper around ChromaDB for storing document embeddings and performing semantic similarity searches.

### Features

- **Persistent Storage**: Uses ChromaDB with persistent storage for production deployment
- **Document Management**: Add documents with embeddings and metadata
- **Similarity Search**: Find top-k most similar documents using cosine similarity
- **Error Handling**: Comprehensive validation and error handling
- **Collection Management**: Create, clear, and manage document collections

### Usage

```python
from services.vector_store import VectorStore

# Initialize the vector store
vector_store = VectorStore(
    persist_directory="/app/chroma_data",
    collection_name="resume_chunks"
)

# Add documents with embeddings
texts = [
    "Python programming and web development",
    "Machine learning and AI technologies",
    "Database design and optimization"
]
embeddings = [
    [0.1] * 384,  # 384-dimensional embedding
    [0.2] * 384,
    [0.3] * 384
]
metadatas = [
    {"section": "skills", "subsection": "languages"},
    {"section": "experience", "subsection": "ai_ml"},
    {"section": "projects", "subsection": "project_1"}
]

vector_store.add_documents(texts, embeddings, metadatas)

# Perform similarity search
query_embedding = [0.15] * 384
results = vector_store.similarity_search(query_embedding, k=3)

for text, score in results:
    print(f"Score: {score:.4f} | Text: {text}")

# Get collection count
count = vector_store.get_collection_count()
print(f"Total documents: {count}")

# Clear collection (for re-indexing)
vector_store.clear_collection()
```

### Methods

#### `__init__(persist_directory: str = "/app/chroma_data", collection_name: str = "resume_chunks")`
Initialize ChromaDB client with persistent storage.

**Parameters:**
- `persist_directory`: Directory path for persistent storage (default: "/app/chroma_data")
- `collection_name`: Name of the collection to store embeddings (default: "resume_chunks")

**Raises:**
- `Exception`: If ChromaDB client initialization fails

**Notes:**
- Creates persist directory if it doesn't exist
- Uses persistent client for production deployment
- Disables telemetry for privacy

#### `add_documents(texts: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]] = None) -> None`
Store document texts with their embeddings in the vector store.

**Parameters:**
- `texts`: List of text chunks to store
- `embeddings`: List of embedding vectors (384-dimensional)
- `metadatas`: Optional list of metadata dictionaries for each document

**Raises:**
- `ValueError`: If texts and embeddings have different lengths
- `ValueError`: If metadatas length doesn't match texts length
- `ValueError`: If embeddings have incorrect dimensions (not 384)
- `Exception`: If document insertion fails

**Notes:**
- Creates collection if it doesn't exist
- Reuses existing collection if available
- Generates unique IDs for each document
- Uses empty metadata if not provided

#### `similarity_search(query_embedding: List[float], k: int = 3) -> List[Tuple[str, float]]`
Find the k most similar documents to the query embedding.

**Parameters:**
- `query_embedding`: Query embedding vector (384-dimensional)
- `k`: Number of results to return (default: 3)

**Returns:**
- List of tuples containing (text_chunk, similarity_score)
- Results are ordered by similarity score in descending order
- Returns empty list if collection is empty or doesn't exist

**Raises:**
- `ValueError`: If query_embedding has incorrect dimensions (not 384)
- `ValueError`: If k is less than 1
- `Exception`: If similarity search fails

**Notes:**
- Uses cosine similarity for matching
- Returns at most k results (or fewer if collection has fewer documents)
- Converts ChromaDB distances to similarity scores (similarity = 1 - distance)

#### `clear_collection() -> None`
Clear all documents from the collection.

**Raises:**
- `Exception`: If collection deletion fails

**Notes:**
- Useful for testing or re-indexing
- Deletes the entire collection
- Sets collection reference to None

#### `get_collection_count() -> int`
Get the number of documents in the collection.

**Returns:**
- Number of documents in the collection, or 0 if collection doesn't exist

**Notes:**
- Safe to call even if collection doesn't exist
- Returns 0 for non-existent collections

### Configuration

The VectorStore uses ChromaDB with the following configuration:

```python
Settings(
    anonymized_telemetry=False,  # Disable telemetry for privacy
    allow_reset=True             # Allow collection reset for testing
)
```

**Collection Metadata:**
```python
{
    "description": "Resume content embeddings for RAG",
    "embedding_model": "all-MiniLM-L6-v2",
    "embedding_dimension": 384
}
```

### Requirements Validation

This implementation validates the following requirements:

- **Requirement 4.3**: Stores embeddings with associated resume text chunks
- **Requirement 4.6**: Supports similarity search queries returning top-k results
- **Requirement 12.6**: Indexes embeddings for sub-100ms similarity search

### Testing

Comprehensive tests are available in `tests/test_vector_store.py`:

**Test Categories:**
- Initialization tests (directory creation, custom collection names)
- Document addition tests (basic, with metadata, validation)
- Similarity search tests (ordering, k parameter, edge cases)
- Collection management tests (clear, count)
- Persistence tests (data persists across instances)
- Error handling tests (validation, edge cases)

**Test Coverage:**
- ✓ Basic functionality
- ✓ Metadata handling
- ✓ Input validation
- ✓ Error conditions
- ✓ Edge cases (empty collections, special characters)
- ✓ Persistence across instances
- ✓ Multiple collections in same directory

Run tests with:
```bash
pytest tests/test_vector_store.py -v
```

### Error Handling

The service includes comprehensive error handling:

**Validation Errors:**
- Mismatched lengths between texts, embeddings, and metadatas
- Incorrect embedding dimensions (must be 384)
- Invalid k parameter (must be >= 1)

**Runtime Errors:**
- ChromaDB client initialization failures
- Collection creation/access failures
- Document insertion failures
- Query execution failures

**Edge Cases:**
- Empty collections (returns empty results)
- Non-existent collections (returns empty results)
- Requesting more results than available (returns all available)
- Special characters in text (handled gracefully)

### Logging

The service uses Python's logging module to track:

- ChromaDB client initialization
- Collection creation/access
- Document addition operations
- Similarity search operations
- Collection management operations
- Error conditions with details

Configure logging in your application:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Performance Considerations

**Storage:**
- Persistent storage ensures data survives restarts
- Directory path configurable for different environments
- Collection-based organization for multiple datasets

**Search Performance:**
- ChromaDB optimized for fast similarity search
- Sub-100ms query times for typical resume corpus
- Cosine similarity for semantic matching

**Memory:**
- Persistent client loads data on demand
- Efficient storage of 384-dimensional vectors
- Metadata stored alongside embeddings

### Integration with RAG Pipeline

The VectorStore integrates with the RAG pipeline:

1. **Initialization**: EmbeddingService generates embeddings from resume.json
2. **Storage**: VectorStore stores embeddings with text chunks
3. **Query**: User question converted to embedding by EmbeddingService
4. **Retrieval**: VectorStore finds top-k similar chunks
5. **Context**: Retrieved chunks used to construct LLM prompt

Example integration:
```python
# Initialize services
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Index resume data
embeddings_with_chunks = embedding_service.embed_resume_corpus()
texts = [chunk for chunk, _ in embeddings_with_chunks]
embeddings = [emb for _, emb in embeddings_with_chunks]
vector_store.add_documents(texts, embeddings)

# Query pipeline
question = "What projects has the candidate worked on?"
query_embedding = embedding_service.generate_embedding(question)
relevant_chunks = vector_store.similarity_search(query_embedding, k=3)

# Use chunks for RAG
context = "\n".join([text for text, _ in relevant_chunks])
```

### Production Deployment

**Storage Path:**
- Default: `/app/chroma_data` (suitable for Docker containers)
- Configurable via constructor parameter
- Ensure directory has write permissions

**Environment Variables:**
```bash
# Optional: Configure storage path
CHROMA_PERSIST_DIRECTORY=/app/chroma_data
```

**Docker Volume:**
```yaml
volumes:
  - chroma_data:/app/chroma_data
```

**Railway Deployment:**
- Persistent storage supported via Railway volumes
- Data persists across deployments
- Automatic directory creation on first run
