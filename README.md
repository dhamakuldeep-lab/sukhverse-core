# Sukverse – Modular Learning Platform (Refactored)

This repository provides a clean microservices implementation of the Sukverse Workshop Learning Platform.  It follows domain‑driven design and isolates concerns into six microservices communicating via REST and Kafka events.  Each service has its own PostgreSQL database and is deployed as an independent container.

## Services

| Service | Description | Port |
|--------|-------------|------|
| **auth_service** | Handles user registration, login, refresh tokens and role/permission management.  Owns the identity tables and emits events on user actions. | `8000` |
| **user_mgmt_service** | Admin interface to manage user profiles, assign roles and process CSV uploads.  Fetches identity data from auth service via REST. | `8001` |
| **workshop_service** | Manages workshops, steps, substeps and tracks student progress.  Emits events when students complete steps. | `8002` |
| **quiz_service** | Provides a reusable quiz engine: define quizzes, questions and capture student attempts.  Emits events on quiz completion. | `8003` |
| **analytics_service** | Consumes progress and quiz events to compute completion percentages, average scores and at‑risk students. | `8004` |
| **certificate_service** | Listens for completion events and issues certificates based on templates and completion criteria. | `8005` |

## Running the Platform

1. Install Docker and Docker Compose.
2. Copy each `.env.example` file to `.env` under its respective service folder and update secrets/connection strings as needed.
3. Run `docker-compose up --build` from the project root.  This will start each service, PostgreSQL databases, Zookeeper and Kafka.
4. Access the API endpoints on the ports listed above.  Each FastAPI service exposes an OpenAPI spec at `/docs`.

## Directory Structure

Each service is self‑contained.  For example, the `auth_service` is organised as:

```
auth_service/
  ├─ app/
  │   ├─ api/            # FastAPI route definitions
  │   ├─ models/         # SQLAlchemy ORM models
  │   ├─ schemas/        # Pydantic request/response models
  │   ├─ services/       # Business logic (JWT, registration, tokens)
  │   ├─ utils/          # Utility functions (password hashing)
  │   ├─ events/         # Kafka producer/consumer utilities
  │   └─ main.py         # FastAPI application entrypoint
  ├─ requirements.txt
  ├─ Dockerfile
  └─ .env.example
```

All other services follow a similar layout, customised for their domain.

### Auth Service API

The auth service exposes a `/auth/refresh` endpoint. Send a JSON body containing
`{"refresh_token": "<token>"}` to obtain a new access token when the previous
one expires. Tables, including `refresh_tokens`, are automatically created on
startup.