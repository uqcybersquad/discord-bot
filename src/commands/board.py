import os
import discord
import messages

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
GITHUB_LINK = os.getenv('GITHUB')
RATE_COOLDOWN = os.getenv('RATE_COOLDOWN')

# Doing it this way to allow future modifications
msg = messages.Messages()

class Board(commands.Cog):
    """
    To-do list similar to Trello board but for Dicord.
    """
    def __init__(self, bot):
        self._bot = bot


def setup(bot):
        bot.add_cog(Board(bot))
