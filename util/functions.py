import os
import dotenv

class BotStuff:
    def __init__(self):
        dotenv.load_dotenv()

    def load_token(self):
        return os.getenv('DISCORD_LOGIN_TOKEN')

