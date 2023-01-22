import aiosqlite
import asyncio

async def main():
    async with aiosqlite.connect("suggestions.db") as db:
        async with db.execute("CREATE TABLE IF NOT EXIST views (message_id INTEGER, voted TEXT)") as create:
            await db.commit()

asyncio.run(main())