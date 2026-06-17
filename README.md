# habit-analytics-platform
Habit analytics backend built with FastAPI.

## Clone repo
```bash
git clone https://github.com/Warghz/habit-analytics-platform.git 
cd habit-analytics-platform
```
## Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

## Install requirements

```bash
pip install -r requirements.txt
```

## Run development server

```bash
uvicorn app.main:app --reload
```

### server will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Structure

```text
app/
│
├── main.py                      # Entry point приложения (FastAPI app + routers)
│
├── api/                         # ВСЕ HTTP слой (routers + dependencies)
│   │
│   ├── __init__.py
│   │
│   ├── routers/                 # REST endpoints
│   │   ├── habits.py           # CRUD habits routes
│   │   ├── habit_log.py        # log / streak routes
│   │   ├── admin.py            # admin-only routes (users/habits management)
│   │   └── __init__.py
│   │
│   ├── dependencies.py         # DI (FastAPI Depends)
│   │   # get_session
│   │   # get_current_user
│   │   # require_admin
│   │   # get_habit_service (если используешь service injection)
│   │
│   └── main.py (optional)     # сборка router include_router()
│
├── core/                        # "ядро" приложения (не зависит от FastAPI логики)
│   │
│   ├── config.py               # settings (env, pydantic settings)
│   ├── database.py             # engine + sessionmaker + get_session
│   ├── security.py             # JWT, hashing, auth utils
│   ├── dependencies.py         # auth deps (get_current_user, require_admin)
│   ├── exceptions.py           # custom exceptions (HabitNotFoundError etc.)
│   └── __init__.py
│
├── models/                      # SQLAlchemy models
│   ├── habits.py
│   ├── habit_logs.py
│   ├── users.py
│   └── __init__.py
│
├── schemas/                     # Pydantic DTO
│   ├── habits.py
│   ├── users.py
│   ├── habit_log.py
│   └── __init__.py
│
├── repositories/                # DATA ACCESS LAYER (DB queries only)
│   ├── habits.py
│   ├── habit_log.py
│   ├── users.py
│   └── __init__.py
│
├── services/                    # BUSINESS LOGIC (NO SQL here ideally)
│   ├── habits.py
│   ├── habit_log.py
│   ├── analytics.py
│   └── __init__.py
│
├── analytics/                   # (optional) heavy computations / pandas
│   ├── streaks.py
│   ├── heatmap.py
│   └── __init__.py
│
├── utils/                       # helper functions (pure functions only)
│   └── __init__.py
│
└── tests/                       # TEST LAYER
    │
    ├── conftest.py             # fixtures (DB, mocks, auth overrides)
    │
    ├── unit/                   # isolated tests (services, analytics)
    │   ├── test_habits.py
    │   ├── test_habit_log.py
    │   ├── test_core.py
    │   └── test_analytics.py
    │
    ├── integration/            # repo + DB (optional real DB / test DB)
    │   ├── test_repositories.py
    │
    ├── api/                    # router tests (httpx AsyncClient)
    │   ├── test_habits_routes.py
    │   ├── test_admin_routes.py
    │   └── test_habit_log_routes.py
    │
    └── fixtures/               # optional reusable fake objects
        └── habits.py
```