# SMS Transaction REST API Documentation

## Overview

This REST API provides secure access to SMS transaction data from a mobile money service. The API implements CRUD operations with Basic Authentication for security.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses Basic Authentication. Include the following header in all requests:

```
Authorization: Basic <base64_encoded_credentials>
```

**Default Credentials:**
- Username: `admin`
- Password: `password123`

**Base64 Encoded:** `YWRtaW46cGFzc3dvcmQxMjM=`

## Endpoints

### 1. List All Transactions

**GET** `/transactions`

Retrieves all SMS transactions.

#### Request Example
```bash
curl -X GET "http://localhost:8000/transactions" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

#### Response Example
```json
{
  "transactions": [
    {
      "id": 1,
      "type": "deposit",
      "amount": 50000,
      "sender": "+250788123456",
      "receiver": "+250788654321",
      "timestamp": "2024-01-15T10:30:00Z",
      "status": "completed",
      "description": "Mobile money deposit"
    },
    {
      "id": 2,
      "type": "withdrawal",
      "amount": 25000,
      "sender": "+250788654321",
      "receiver": "+250788123456",
      "timestamp": "2024-01-15T11:15:00Z",
      "status": "completed",
      "description": "ATM withdrawal"
    }
  ],
  "count": 25
}
```

#### Status Codes
- `200 OK` - Success
- `401 Unauthorized` - Invalid credentials
- `500 Internal Server Error` - Server error

---

### 2. Get Specific Transaction

**GET** `/transactions/{id}`

Retrieves a specific transaction by ID.

#### Path Parameters
- `id` (integer, required) - Transaction ID

#### Request Example
```bash
curl -X GET "http://localhost:8000/transactions/1" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

#### Response Example
```json
{
  "id": 1,
  "type": "deposit",
  "amount": 50000,
  "sender": "+250788123456",
  "receiver": "+250788654321",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "completed",
  "description": "Mobile money deposit"
}
```

#### Status Codes
- `200 OK` - Success
- `400 Bad Request` - Invalid transaction ID format
- `401 Unauthorized` - Invalid credentials
- `404 Not Found` - Transaction not found
- `500 Internal Server Error` - Server error

---

### 3. Create New Transaction

**POST** `/transactions`

Creates a new SMS transaction.

#### Request Body
```json
{
  "type": "deposit",
  "amount": 75000,
  "sender": "+250788111111",
  "receiver": "+250788222222",
  "timestamp": "2024-01-16T14:30:00Z",
  "status": "completed",
  "description": "New mobile deposit"
}
```

#### Required Fields
- `type` (string) - Transaction type (deposit, withdrawal, transfer, payment)
- `amount` (integer) - Transaction amount
- `sender` (string) - Sender phone number
- `receiver` (string) - Receiver phone number
- `timestamp` (string) - Transaction timestamp (ISO 8601 format)
- `status` (string) - Transaction status (completed, pending, failed)
- `description` (string) - Transaction description

#### Request Example
```bash
curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "deposit",
    "amount": 75000,
    "sender": "+250788111111",
    "receiver": "+250788222222",
    "timestamp": "2024-01-16T14:30:00Z",
    "status": "completed",
    "description": "New mobile deposit"
  }'
```

#### Response Example
```json
{
  "id": 26,
  "type": "deposit",
  "amount": 75000,
  "sender": "+250788111111",
  "receiver": "+250788222222",
  "timestamp": "2024-01-16T14:30:00Z",
  "status": "completed",
  "description": "New mobile deposit"
}
```

#### Status Codes
- `201 Created` - Transaction created successfully
- `400 Bad Request` - Invalid JSON data or missing required fields
- `401 Unauthorized` - Invalid credentials
- `500 Internal Server Error` - Server error

---

### 4. Update Transaction

**PUT** `/transactions/{id}`

Updates an existing transaction.

#### Path Parameters
- `id` (integer, required) - Transaction ID

#### Request Body
```json
{
  "type": "deposit",
  "amount": 100000,
  "status": "completed",
  "description": "Updated description"
}
```

**Note:** All fields are optional. Only provided fields will be updated.

#### Request Example
```bash
curl -X PUT "http://localhost:8000/transactions/1" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100000,
    "status": "completed",
    "description": "Updated mobile money deposit"
  }'
```

#### Response Example
```json
{
  "id": 1,
  "type": "deposit",
  "amount": 100000,
  "sender": "+250788123456",
  "receiver": "+250788654321",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "completed",
  "description": "Updated mobile money deposit"
}
```

#### Status Codes
- `200 OK` - Transaction updated successfully
- `400 Bad Request` - Invalid JSON data or transaction ID format
- `401 Unauthorized` - Invalid credentials
- `404 Not Found` - Transaction not found
- `500 Internal Server Error` - Server error

---

### 5. Delete Transaction

**DELETE** `/transactions/{id}`

Deletes a specific transaction.

#### Path Parameters
- `id` (integer, required) - Transaction ID

#### Request Example
```bash
curl -X DELETE "http://localhost:8000/transactions/1" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

#### Response Example
```json
{
  "message": "Transaction 1 deleted successfully",
  "status_code": 200
}
```

#### Status Codes
- `200 OK` - Transaction deleted successfully
- `400 Bad Request` - Invalid transaction ID format
- `401 Unauthorized` - Invalid credentials
- `404 Not Found` - Transaction not found
- `500 Internal Server Error` - Server error

---

## Error Responses

### Unauthorized (401)
```json
{
  "error": "Unauthorized",
  "message": "Authentication required",
  "status_code": 401
}
```

### Bad Request (400)
```json
{
  "error": "Invalid JSON data",
  "status_code": 400
}
```

### Not Found (404)
```json
{
  "error": "Transaction with ID 999 not found",
  "status_code": 404
}
```

### Internal Server Error (500)
```json
{
  "error": "Internal server error",
  "status_code": 500
}
```

---

## Data Models

### Transaction Object
```json
{
  "id": 1,
  "type": "deposit",
  "amount": 50000,
  "sender": "+250788123456",
  "receiver": "+250788654321",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "completed",
  "description": "Mobile money deposit"
}
```

#### Field Descriptions
- `id` (integer) - Unique transaction identifier
- `type` (string) - Transaction type: deposit, withdrawal, transfer, payment
- `amount` (integer) - Transaction amount in local currency
- `sender` (string) - Sender's phone number
- `receiver` (string) - Receiver's phone number
- `timestamp` (string) - Transaction timestamp in ISO 8601 format
- `status` (string) - Transaction status: completed, pending, failed
- `description` (string) - Human-readable transaction description

---

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## CORS Support

The API includes CORS headers to support cross-origin requests from web applications.

## Security Considerations

### Basic Authentication Limitations
- Credentials are transmitted in base64 encoding (not encrypted)
- No session management or token expiration
- Credentials are hardcoded (not suitable for production)

### Recommended Security Improvements
1. **JWT (JSON Web Tokens)** - Stateless authentication with expiration
2. **OAuth 2.0** - Industry standard for API authentication
3. **HTTPS** - Encrypt all communications
4. **Rate Limiting** - Prevent abuse and DoS attacks
5. **Input Validation** - Sanitize all inputs
6. **Audit Logging** - Track all API access

---

## Testing

### Using curl
```bash
# Test authentication
curl -X GET "http://localhost:8000/transactions" \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="

# Test without authentication (should return 401)
curl -X GET "http://localhost:8000/transactions"
```

### Using Postman
1. Set Authorization to "Basic Auth"
2. Username: `admin`
3. Password: `password123`
4. Make requests to the endpoints above

---

## Setup Instructions

1. Install Python 3.7+
2. Navigate to the project directory
3. Run the API server:
   ```bash
   python api/rest_api.py --port 8000
   ```
4. Test the endpoints using curl or Postman

---

## Support

For issues or questions, please refer to the project documentation or contact the development team.
