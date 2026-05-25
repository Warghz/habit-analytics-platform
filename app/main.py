from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

my_habits = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1234},
    {"title": "drink water", "content": "drink water every day", "id": 2}
]


def find_habit(id: int):
    for habit in my_habits:
        if habit['id'] == id:
            return habit

def find_habit_index(id: int):
    for i, habit in enumerate(my_habits):
        if id == habit['id']:
            return i

class Habit(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]

@app.get('/')
def root():
    return {"message": "welcome to my API"}


@app.get('/posts')
def get_habits():
    return {"data": my_habits}


@app.get('/posts/{id}')
def get_habit(id: int):
    habit = find_habit(id)
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"habit with {id} is not exist")

    return {"habit_name": habit['title']}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_habit(habit: Habit):
    habit_dict = habit.dict()
    habit_dict['id'] = randrange(0, 100000000)
    my_habits.append(habit_dict)
    return {'data': habit_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(id: int):
    index = find_habit_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"habit with id: {id} is not found"
        )

    my_habits.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)