from fastapi import APIRouter, Depends, HTTPException, status
# from psycopg import AsyncConnection # TO DO: ПОНЯТЬ ПОЧЕМУ НЕ ИСПОЛЬЗУЕМ
from psycopg.rows import dict_row
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import HabitOut, HabitCreate, HabitUpdate
from ..database import get_session

router = APIRouter()

@router.get('/habits', response_model=list[HabitOut])
async def get_habits(conn: AsyncSession = Depends(get_session)):

    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute("""
        SELECT id, name, content, rating, must_have, created_at 
        FROM habits
        """)
        rows = await cur.fetchall()

    return rows


@router.get('/habits/{habit_id}', response_model=HabitOut)
async def get_habit_by_id(
        habit_id: int,
        conn: AsyncConnection = Depends(get_connection)
):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute("""
        SELECT id, name, content, rating, must_have, created_at
        FROM habits
        WHERE id = %s
        """, (habit_id,))

        row = await cur.fetchone()

        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: habit not found")

        return row


@router.post("/habits", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
        habit: HabitCreate,
        conn: AsyncConnection = Depends(get_connection)
):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute("""
        INSERT INTO habits (name, content, rating, must_have) 
        VALUES (%s, %s, %s, %s) 
        RETURNING * 
        """, (
            habit.name,
            habit.content,
            habit.rating,
            habit.must_have
        ))

        row = await cur.fetchone()
        await conn.commit()

        return row


@router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
        habit_id: int,
        conn: AsyncConnection = Depends(get_connection)
):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute("""
        DELETE FROM habits  
        WHERE id = %s
        RETURNING id
        """, (habit_id,))

        row = await cur.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: habit not found"
            )
        await conn.commit()

        return


@router.put("/habits/{habit_id}", response_model=HabitOut)
async def put_habit(
        habit_id: int,
        habit: HabitUpdate,
        conn: AsyncConnection = Depends(get_connection)
):
    async with conn.cursor(row_factory=dict_row) as cur:
        update_data = habit.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(400, "No fields to update")
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        values = list(update_data.values()) + [habit_id]
        await cur.execute(f"""
            UPDATE habits
            SET {set_clause}
            WHERE id = %s
            RETURNING *
        """, values)

        row = await cur.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: habit not found'
            )

        await conn.commit()

        return row