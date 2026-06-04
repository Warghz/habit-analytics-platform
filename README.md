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
├── core/
│ ├── config.py
│ ├── security.py
│ └── dependencies.py
├── routers/
│ └── auth.py
├── services/
│ └── auth_service.py
├── models/
├── schemas/
└── utils/
```