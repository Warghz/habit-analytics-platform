# Habit Analytics Platform

FastAPI backend for habit tracking, habit logs, streaks, and habit analytics.

## Setup

```bash
git clone https://github.com/Warghz/habit-analytics-platform.git
cd habit-analytics-platform
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create environment variables from `.env.example` and set production-safe values.

## Environment

```text
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/fastapi
ALEMBIC_DATABASE_URL=postgresql+psycopg://postgres:password@localhost/fastapi
SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Database

```bash
alembic upgrade head
```

## Run

```bash
uvicorn app.api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Tests

```bash
.\.venv\Scripts\python.exe -m pytest
```

The test suite covers:

- unit tests for core security, habit services, habit log services, and analytics
- integration tests for habit and habit log repositories
- API tests for auth, habits, habit logs, users, and admin routes

## Project Structure

```text
app/
  analytics/       Habit analytics and heatmap rendering
  api/             FastAPI app assembly and dependency helpers
  core/            Config, database, security, exceptions
  models/          SQLAlchemy models
  repositories/    Data access layer
  routers/         HTTP routes
  schemas/         Pydantic schemas
  services/        Business logic
  tests/           Unit, integration, and API tests
alembic/           Database migrations
```
