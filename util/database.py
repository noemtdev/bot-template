import aiosqlite
from discord.ext import tasks

class Database:
    def __init__(self, bot, path):
        self.bot = bot
        self.path = path
        self.init.start()

    @tasks.loop(count=1)
    async def init(self):
        self.db = await aiosqlite.connect(self.path)

    async def close(self):
        await self.db.commit()
        await self.db.close()

    async def execute(self, query, *args):
        return await self.db.execute(query, *args)

    async def fetchone(self, cursor):
        return await cursor.fetchone()

    async def fetchall(self, cursor):
        return await cursor.fetchall()

    async def commit(self):
        await self.db.commit()

        

    