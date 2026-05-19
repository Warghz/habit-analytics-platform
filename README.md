# habit-analytics-platform
Habit analytics backend built with FastAPI, PostgreSQL and pandas

# Clone repo
git clone https://github.com/Warghz/habit-analytics-platform.git
cd habit-analytics-platform

# Create and activate virualenv
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run develepment server
uvicorn app.main:app --reload
## server will run at:
http://127.0.0.1:8000

# API Documentation
## UI swagger:
http://127.0.0.1:8000/docs
