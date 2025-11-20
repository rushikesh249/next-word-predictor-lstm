# API Documentation

## Base URL
```
http://127.0.0.1:5000
```

## Endpoints

### Health Check
Check if the backend server is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200` - Server is healthy
- `500` - Server error

---

### Predict Next Words
Generate next word predictions using the LSTM model.

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "text": "your input text",
  "num_words": 3
}
```

**Parameters:**
- `text` (string, required) - Input text prompt (2-5 words recommended)
- `num_words` (integer, optional) - Number of words to predict (1-10, default: 1)

**Response:**
```json
{
  "completion": "predicted words here",
  "words": ["predicted", "words", "here"]
}
```

**Response Fields:**
- `completion` (string) - Complete predicted text
- `words` (array) - Individual predicted words

**Status Codes:**
- `200` - Successful prediction
- `400` - Invalid request (missing text)
- `500` - Server error

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "the quick brown", "num_words": 3}'
```

**Example Response:**
```json
{
  "completion": "fox jumps over",
  "words": ["fox", "jumps", "over"]
}
```

## Error Handling

All endpoints return JSON error responses in the following format:

```json
{
  "error": "Error message description"
}
```

Common error scenarios:
- Empty text input
- Invalid num_words parameter
- Model not trained
- Server internal errors
