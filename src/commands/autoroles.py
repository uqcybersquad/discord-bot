import os
import discord

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
GITHUB_LINK = os.getenv('GITHUB')
RATE_COOLDOWN = os.getenv('RATE_COOLDOWN')

roles = {
    # meg id, role id

}


class AutoRole(commands.Cog):
    """
    Listeners to track reaction autoroles.
    """
    def __init__(self, bot):
        self._bot = bot
        self.roles = {}


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

def setup(bot):
        bot.add_cog(AutoRole(bot))
