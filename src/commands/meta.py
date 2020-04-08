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

    """
    Get interesting discord stats and send to channel
    TODO: WIP
    """
    @commands.command(name="stats")
    async def get_discord_stats(self, ctx):
        msg = ""
        guild = ctx.guild

        memberCount = len(guild.members)
        onlineMemberCount = len([mem for mem in guild.members if mem.status == discord.Status.online])
        
        msg += f"<:hellothere:679599404818235393>There are {onlineMemberCount} of {memberCount} people online!" 

        await ctx.send(msg)
        


def setup(bot):
	bot.add_cog(Meta(bot))