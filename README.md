# Taskion - Simple FastAPI To-Do Application

A minimal FastAPI application for managing tasks with CRUD operations using MontyDB (SQLite engine) for storage.

## Dependencies

- Python 3.12+
- [Poetry](https://python-poetry.org/)

## Quick Start

```bash
# Install dependencies
poetry install --with=dev

# Run the application
poetry run python src/main.py
# Or: python run.py (after poetry shell)

# Access the API
open http://localhost:8930/docs
```

## Features

- ✅ Complete CRUD operations for tasks
- ✅ Pydantic validation (title 1-100 chars, description max 500 chars)
- ✅ MontyDB (SQLite) storage
- ✅ Clean project structure following best practices
- ✅ Comprehensive test coverage
- ✅ Type hints throughout

## API Endpoints

| Method | Endpoint      | Description                              |
| ------ | ------------- | ---------------------------------------- |
| GET    | `/health`     | Health check → `{"status": "ok"}`        |
| POST   | `/tasks/`     | Create task (201 + TaskOut)              |
| GET    | `/tasks/`     | List tasks (with ?done, ?limit, ?offset) |
| GET    | `/tasks/{id}` | Get task by ID (404 if not found)        |
| PUT    | `/tasks/{id}` | Update task (404 if not found)           |
| DELETE | `/tasks/{id}` | Delete task (204 if success)             |

## Data Models

**TaskCreate (Request)**
```json
{
  "title": "string (1-100 chars, required)",
  "description": "string (max 500 chars, optional)",
  "done": "boolean (default: false)"
}
```

**TaskOut (Response)**
```json
{
  "id": "string",
  "title": "string",
  "description": "string|null",
  "done": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Testing

```bash
poetry run pytest                                      # Run all tests
poetry run pytest --cov=src  --cov-report=term-missing # With coverage
```

## Project Structure

```shell
taskion/
├── src/
│   ├── app.py                 # FastAPI app
│   ├── main.py                # Entry point (port 8930)
│   └── apps/
│       ├── health/            # Health check
│       └── tasks/             # Task CRUD
└── tests/                     # 3 clean test files
    ├── test_api.py            # API endpoint tests
    ├── test_models.py         # Database & Pydantic models
    └── test_integration.py    # End-to-end tests
```

Built for code review, learning FastAPI, and recruiting exercises.