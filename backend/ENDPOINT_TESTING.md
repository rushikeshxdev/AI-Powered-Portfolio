# GET /api/chat/history/{session_id} Endpoint Testing Guide

## Endpoint Overview

**URL**: `GET /api/chat/history/{session_id}`

**Purpose**: Retrieve chat history for a specific session

**Response Model**: `ChatHistoryResponse`

## Parameters

### Path Parameters
- `session_id` (string, required): Chat session identifier in UUID format
  - Example: `123e4567-e89b-12d3-a456-426614174000`

### Query Parameters
- `limit` (integer, optional): Maximum number of messages to retrieve
  - Default: 50
  - Minimum: 1
  - Maximum: 100

## Response Format

```json
{
  "messages": [
    {
      "id": 1,
      "session_id": "123e4567-e89b-12d3-a456-426614174000",
      "role": "user",
      "content": "What projects has Rushikesh worked on?",
      "timestamp": "2024-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "session_id": "123e4567-e89b-12d3-a456-426614174000",
      "role": "assistant",
      "content": "Rushikesh has worked on several projects...",
      "timestamp": "2024-01-01T10:00:05Z"
    }
  ],
  "total": 2
}
```

## Testing with cURL

### 1. Basic Request (Default Limit)
```bash
curl -X GET "http://localhost:8000/api/chat/history/123e4567-e89b-12d3-a456-426614174000"
```

### 2. Request with Custom Limit
```bash
curl -X GET "http://localhost:8000/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=10"
```

### 3. Request with Maximum Limit
```bash
curl -X GET "http://localhost:8000/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=100"
```

## Expected Responses

### Success (200 OK)
```json
{
  "messages": [...],
  "total": 2
}
```

### Empty History (200 OK)
```json
{
  "messages": [],
  "total": 0
}
```

### Invalid UUID Format (422 Unprocessable Entity)
```json
{
  "detail": "session_id must be a valid UUID format"
}
```

### Invalid Limit (422 Unprocessable Entity)
```bash
# Limit below minimum (0)
curl -X GET "http://localhost:8000/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=0"

# Limit above maximum (101)
curl -X GET "http://localhost:8000/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=101"
```

Response:
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["query", "limit"],
      "msg": "Input should be greater than or equal to 1",
      "input": "0"
    }
  ]
}
```

### Server Error (500 Internal Server Error)
```json
{
  "detail": "Failed to retrieve chat history"
}
```

## Implementation Details

### Features
1. **UUID Validation**: Validates session_id is in proper UUID format
2. **Limit Enforcement**: Enforces limit constraints (1-100) via FastAPI Query validation
3. **Ascending Order**: Returns messages ordered by timestamp (oldest first)
4. **Empty History Handling**: Returns empty list (not 404) for sessions with no messages
5. **Error Handling**: Graceful error handling with appropriate HTTP status codes

### Database Query
- Uses `ChatRepository.get_history()` method
- Queries messages filtered by session_id
- Orders by timestamp ascending
- Applies limit constraint

### Response Construction
- Converts SQLAlchemy ORM models to Pydantic models
- Returns `ChatHistoryResponse` with messages and total count
- Total count matches the number of messages returned

## Testing Checklist

- [x] Valid UUID with messages returns 200 with message list
- [x] Valid UUID with no messages returns 200 with empty list
- [x] Invalid UUID format returns 422
- [x] Limit parameter defaults to 50
- [x] Limit parameter respects custom values (1-100)
- [x] Limit below 1 returns 422
- [x] Limit above 100 returns 422
- [x] Messages are ordered by timestamp ascending
- [x] Response includes all required fields (id, session_id, role, content, timestamp)
- [x] Database errors return 500 with error message

## Integration with Frontend

The frontend can use this endpoint to:
1. Load chat history when user returns to a session
2. Display previous conversations
3. Implement pagination for long chat histories
4. Restore context for continued conversations

Example frontend usage:
```typescript
async function loadChatHistory(sessionId: string, limit: number = 50) {
  const response = await fetch(
    `http://localhost:8000/api/chat/history/${sessionId}?limit=${limit}`
  );
  
  if (!response.ok) {
    throw new Error('Failed to load chat history');
  }
  
  const data = await response.json();
  return data.messages;
}
```
