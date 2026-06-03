import asyncpg
import asyncio

async def test():
    conn = await asyncpg.connect(
        user="postgres",
        password="YOUR_PASSWORD",
        database="habits",
        host="127.0.0.1",
        port=5432
    )
    print("CONNECTED OK")
    await conn.close()

asyncio.run(test())