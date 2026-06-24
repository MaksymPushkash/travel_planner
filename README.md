# Travel Planner API

Simple FastAPI application for managing travel projects and places from the Art Institute of Chicago API.

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Docker / Docker Compose
* JWT Authentication
* Pydantic
* HTTPX

## Features

* User registration
* User login with JWT token
* Create, read, update and delete travel projects
* Add places to travel projects from external API
* Update notes for project places
* Mark places as visited
* Automatically mark project as completed when all places are visited
* Prevent deleting a project if it has visited places
* Prevent adding the same place twice to one project
* Maximum 10 places per project

## Project Structure

```text
app/
├── api/
├── clients/
├── core/
├── database/
├── models/
├── repositories/
├── schemas/
├── services/
└── main.py
```

## Environment Variables

Create `.env` file:

```env
DB_NAME=travel_planner
DB_USER=postgres
DB_PASSWORD=postgres

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/travel_planner

JWT_SECRET_KEY=super-secret-key-change-me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

ART_INSTITUTE_API_BASE_URL=https://api.artic.edu/api/v1

PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

## Run with Docker

```bash
docker compose up --build
```

API will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

PgAdmin:

```text
http://localhost:5050
```

## Run migrations

If migrations are not applied automatically, run:

```bash
docker compose exec app alembic upgrade head
```

Create a new migration:

```bash
uv run alembic revision --autogenerate -m "migration message"
```

Apply migration locally:

```bash
uv run alembic upgrade head
```

## API Endpoints

### Auth

| Method | Endpoint                | Description              |
| ------ | ----------------------- | ------------------------ |
| POST   | `/api/v1/auth/register` | Register user            |
| POST   | `/api/v1/auth/login`    | Login user               |
| POST   | `/api/v1/auth/token`    | Login for Swagger OAuth2 |
| GET    | `/api/v1/auth/me`       | Get current user         |

### Projects

| Method | Endpoint                        | Description    |
| ------ | ------------------------------- | -------------- |
| POST   | `/api/v1/projects`              | Create project |
| GET    | `/api/v1/projects`              | List projects  |
| GET    | `/api/v1/projects/{project_id}` | Get project    |
| PATCH  | `/api/v1/projects/{project_id}` | Update project |
| DELETE | `/api/v1/projects/{project_id}` | Delete project |

### Places

| Method | Endpoint                                          | Description  |
| ------ | ------------------------------------------------- | ------------ |
| POST   | `/api/v1/projects/{project_id}/places`            | Add place    |
| GET    | `/api/v1/projects/{project_id}/places`            | List places  |
| GET    | `/api/v1/projects/{project_id}/places/{place_id}` | Get place    |
| PATCH  | `/api/v1/projects/{project_id}/places/{place_id}` | Update place |

## Example Requests

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Create Project

```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Chicago Trip",
    "description": "Art places I want to visit",
    "start_date": "2026-07-01",
    "places": []
  }'
```

### Add Place

```bash
curl -X POST http://localhost:8000/api/v1/projects/1/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "external_place_id": 129884,
    "notes": "I want to visit this artwork"
  }'
```

### Mark Place as Visited

```bash
curl -X PATCH http://localhost:8000/api/v1/projects/1/places/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "is_visited": true
  }'
```

## Business Rules

* A project can have up to 10 places.
* The same external place cannot be added twice to the same project.
* A project cannot be deleted if it has at least one visited place.
* When all places in a project are visited, the project is automatically marked as completed.

## Development

Run linting:

```bash
uv run ruff check
```

Run formatting:

```bash
uv run ruff format
```

Run type checking:

```bash
uv run mypy app
```

## External API

This project uses the Art Institute of Chicago API:

```text
https://api.artic.edu/api/v1
```

Example artwork ID for testing:

```text
129884
```
