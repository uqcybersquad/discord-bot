import discord
from discord.ext import commands

GITHUB_LINK = "https://github.com/uqcybersquad/discord-bot"

"""
Meta commands such as statistics, bot info, etc.
"""
class Meta(commands.Cog):

    def __init__(self, bot):
        self._bot = bot

    """
    Send developers link to github channel
    """
    @commands.command(name="link")
    async def get_github_link(self, ctx):
        await ctx.send(GITHUB_LINK)


def setup(bot):
	bot.add_cog(Meta(bot))