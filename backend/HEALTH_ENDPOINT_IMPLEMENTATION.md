# Health Endpoint Implementation

## Overview

This document describes the implementation of the GET /api/health endpoint as specified in Task 5.7 of the AI Portfolio project.

## Requirements

The health endpoint must:
1. Check database connectivity with SELECT 1 query
2. Check vector store with heartbeat call (get_collection_count)
3. Return status "healthy" or "degraded" with service statuses
4. Return HTTP 200 if healthy, 503 if degraded
5. Validate Requirements 10.6 and 10.7

## Implementation Details

### Endpoint Signature

```python
@app.get("/api/health", response_model=HealthResponse)
async def health_check(
    request: Request,
    db_session: AsyncSession = Depends(get_db)
) -> HealthResponse
```

### Service Checks

#### Database Connectivity
- Executes `SELECT 1` query using SQLAlchemy
- Marks database as available if query succeeds
- Catches exceptions and marks as unavailable on failure
- Logs errors for debugging

```python
try:
    result = await db_session.execute(text("SELECT 1"))
    result.fetchone()
    services["database"] = True
    logger.debug("Database health check: OK")
except Exception as e:
    services["database"] = False
    logger.error(f"Database health check failed: {e}")
```

#### Vector Store Connectivity
- Calls `vector_store.get_collection_count()` method
- Marks vector store as available if call succeeds
- Catches exceptions and marks as unavailable on failure
- Logs errors and collection count for debugging

```python
try:
    vector_store = request.app.state.vector_store
    count = vector_store.get_collection_count()
    services["vector_store"] = True
    logger.debug(f"Vector store health check: OK (count={count})")
except Exception as e:
    services["vector_store"] = False
    logger.error(f"Vector store health check failed: {e}")
```

### Status Determination

The overall health status is determined by checking all service statuses:

```python
all_healthy = all(services.values())
status = "healthy" if all_healthy else "degraded"
```

- **healthy**: All services (database and vector store) are operational
- **degraded**: One or more services are unavailable

### HTTP Status Codes

- **200 OK**: Returned when status is "healthy" (all services operational)
- **503 Service Unavailable**: Returned when status is "degraded" (some services down)

```python
if all_healthy:
    return response
else:
    return JSONResponse(
        status_code=503,
        content=response.model_dump()
    )
```

### Response Schema

The endpoint uses the `HealthResponse` Pydantic model:

```python
class HealthResponse(BaseModel):
    status: str  # "healthy" or "degraded"
    timestamp: datetime  # Auto-generated
    services: Optional[dict]  # {"database": bool, "vector_store": bool}
```

## Example Responses

### All Services Healthy (HTTP 200)

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "services": {
    "database": true,
    "vector_store": true
  }
}
```

### Database Unavailable (HTTP 503)

```json
{
  "status": "degraded",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "services": {
    "database": false,
    "vector_store": true
  }
}
```

### All Services Unavailable (HTTP 503)

```json
{
  "status": "degraded",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "services": {
    "database": false,
    "vector_store": false
  }
}
```

## Error Handling

The implementation handles errors gracefully:

1. **Database Errors**: Caught and logged, service marked as unavailable
2. **Vector Store Errors**: Caught and logged, service marked as unavailable
3. **No Crash**: The endpoint never crashes, always returns a valid response
4. **Logging**: All errors are logged with context for debugging

## Testing

### Manual Testing

Use curl to test the endpoint:

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test with verbose output
curl -v http://localhost:8000/api/health
```

### Unit Tests

Unit tests are provided in `tests/test_main.py`:

- `test_health_check_all_services_healthy()`: Tests healthy state (200)
- `test_health_check_database_unavailable()`: Tests degraded state with DB down (503)
- `test_health_check_vector_store_unavailable()`: Tests degraded state with VS down (503)
- `test_health_check_all_services_unavailable()`: Tests degraded state with all down (503)

### Manual Test Script

Run the manual test script to verify implementation:

```bash
cd backend
python test_health_manual.py
```

## Changes Made

### Files Modified

1. **backend/src/main.py**
   - Added `HealthResponse` to imports
   - Added `text` from sqlalchemy to imports
   - Updated health_check endpoint from `/health` to `/api/health`
   - Added database connectivity check with SELECT 1
   - Added vector store connectivity check with get_collection_count()
   - Added service status tracking
   - Added HTTP 503 response for degraded state

2. **backend/tests/test_main.py**
   - Replaced old `test_health_check()` with four new tests
   - Added mocking for database and vector store
   - Added tests for all service state combinations

3. **backend/README.md**
   - Updated endpoint path from `/health` to `/api/health`
   - Updated expected response format
   - Added service status information

### Files Created

1. **backend/test_health_manual.py**
   - Manual test script for health endpoint logic
   - Tests schema, logic, and imports

2. **backend/HEALTH_ENDPOINT_IMPLEMENTATION.md**
   - This documentation file

## Deployment Considerations

### Railway Deployment

When deploying to Railway, ensure:

1. **Database URL**: Set `DATABASE_URL` environment variable
2. **Vector Store Path**: Ensure `/app/chroma_data` directory exists and is writable
3. **Health Check Configuration**: Configure Railway to use `/api/health` endpoint
4. **Monitoring**: Set up alerts for 503 responses

### Health Check Configuration

In `railway.toml`:

```toml
[deploy]
healthcheckPath = "/api/health"
healthcheckTimeout = 10
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

## Monitoring

The health endpoint can be used for:

1. **Uptime Monitoring**: External services (UptimeRobot, Pingdom)
2. **Load Balancer Health Checks**: Railway, AWS ELB, etc.
3. **Service Discovery**: Kubernetes, Consul, etc.
4. **Alerting**: Trigger alerts on 503 responses

## Compliance

This implementation satisfies:

- **Requirement 10.6**: Backend exposes health check endpoint at /api/health
- **Requirement 10.7**: Health check returns HTTP 200 if all services operational
- **Task 5.7**: Implement GET /api/health endpoint with database and vector store checks

## Future Enhancements

Potential improvements:

1. Add OpenRouter API connectivity check
2. Add response time metrics
3. Add detailed error messages in response
4. Add health check for embedding service
5. Add cache for health check results (avoid checking on every request)
6. Add more granular service status (e.g., "warning" state)
