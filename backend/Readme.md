# Job Search Gamification API

This is a FastAPI-based backend for a job search gamification platform. It provides user management, job search functionality using SerpAPI Google Jobs API, and Firebase integration for data storage.

## v1.0 Backend Features

**User Management**:
- Register and login users with JWT-based authentication.
- Role-based access control (RBAC).
- Manage API keys for SerpAPI integration.

**Job Search**:
- Search for jobs using SerpAPI Google Jobs API.
- Supports pagination for search results.

**Data Storage**:
- Uses Firebase Firestore to store user data, search logs, and job details.

## Setup

### 1. Install Dependencies

Install required dependencies:

```
pip install -r requirements.txt
```

### 2. Run the Server

```
uvicorn main:app --reload
```

API documentation is available at `http://127.0.0.1:8000/docs`.

## API Endpoints

### 1. User Management

**Register**: `POST /v1/user/register`
**Login**: `POST /v1/user/login`
**Add API Key**: `PUT /v1/user/apikey`

### 2. Job Search

**Search Jobs**: `POST /v1/search/jobs`
- Provide `query` and `location` for a new search or `search_id` for pagination.

## Unit & Integration Testing

### Run Tests

Run all tests with `pytest`:

```
pytest v1/tests
```

## Documentation Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SerpAPI Google Jobs API Documentation](https://serpapi.com/google-jobs-api)
- [Firebase Admin SDK Documentation](https://firebase.google.com/docs/reference/admin/python/firebase_admin)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/en/stable/)
