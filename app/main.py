from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


habits = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Habit Analytics API is running"}


@app.get("/health")
def health():
    return {'status': 'ok'}


class Habit(BaseModel):
    name: str


@app.post('/habits')
def create_habit(habit: Habit):
    global next_id

    new_habit = {
        'id': next_id,
        'name': habit.name
    }

    habits.append(new_habit)
    next_id += 1

    return {"message": "Habit created",
            "habit": new_habit
    }


@app.get("/habits")
def get_habits():
    return {
        "count": len(habits),
        "habits": habits
    }

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int):
    for habit in habits:
        if habit['id'] == habit_id:
            habits.remove(habit)
            return {
                'message': "Habit deleted",
                'id': habit_id
            }
    return {
        "message": "Habit not found"
    }