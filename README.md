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
├── core/                 # ядро приложения (самое важное)
│   ├── config.py         # настройки (env, settings)
│   ├── security.py       # JWT, hash_password, decode, create token
│   ├── dependencies.py   # get_current_user, require_admin и т.д.
│
├── database/             # работа с БД
│   ├── session.py        # get_session
│   ├── base.py           # Base SQLAlchemy
│
├── models/               # ORM модели (SQLAlchemy)
│   ├── users.py
│   ├── habits.py
│
├── schemas/              # Pydantic схемы (DTO)
│   ├── users.py
│   ├── auth.py
│   ├── habits.py
│
├── routers/              # API слои (FastAPI endpoints)
│   ├── auth.py
│   ├── users.py
│   ├── habits.py
│
├── services/             # бизнес-логика (ВАЖНО)
│   ├── user_service.py
│   ├── habit_service.py
│
├── repositories/         # (опционально, но топ уровень)
│   ├── user_repo.py
│   ├── habit_repo.py
│
├── utils/                # утилиты (не бизнес логика)
│   ├── helpers.py
│
├── main.py               # entrypoint FastAPI
```