import aiosqlite

from collections import Counter

from config import SQLITE_DB_FILE


async def add_history(user_id: int, movie_name: str) -> None:
    async with aiosqlite.connect(SQLITE_DB_FILE) as db:
        sql = f"""
        INSERT INTO users_history (user_id, movie_name)
        VALUES ({user_id}, '{movie_name}');"""
        await db.execute(sql)
        await db.commit()


async def get_history(user_id: int) -> list[str]:
    sql = f"""
        SELECT DISTINCT movie_name
        FROM users_history
        WHERE user_id = {user_id}"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as db:
        return [i[0] for i in await db.execute_fetchall(sql)]


async def get_stats(user_id: int) -> dict[str, int]:
    sql = f"""
        SELECT movie_name
        FROM users_history
        WHERE user_id = {user_id}"""
    async with aiosqlite.connect(SQLITE_DB_FILE) as db:
        return Counter([i[0] for i in await db.execute_fetchall(sql)])
