from abc import ABC

import discord
from discord.ext import commands

import os
import json

from util.functions import BotStuff
from util.database import Database
from view import SuggestionView

class Bot(commands.Bot, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.botStuff = BotStuff()
        self.token = self.botStuff.load_token()
        self.suggestions_channel = 1066577547116163102
        self.command_prefix = '!'
        self.remove_command('help')
        self.embed_color = discord.Color.blurple()
        self.suggestion_database = Database(self, 'data/suggestions.db')
        self.owner_id = 352793093105254402

    async def on_ready(self):
        await self.load_views()

    def load_commands(self):
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                self.load_extension(f'commands.{filename[:-3]}')

    def run(self):
        self.load_commands()
        super().run(self.token)

    async def load_views(self):
        cur = await bot.suggestion_database.execute("SELECT * FROM views")
        rows = await bot.suggestion_database.fetchall(cur)

        for row in rows:
            voted = json.loads(row[1].replace("'", '"'))
            bot.add_view(SuggestionView(self._bot, row[0], voted))


intents = discord.Intents.default()
bot = Bot(intents=intents)

bot.run()
