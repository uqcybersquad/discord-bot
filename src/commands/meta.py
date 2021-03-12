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

"""
Meta commands such as statistics, bot info, etc.
"""
class Meta(commands.Cog):

    def __init__(self, bot):
        self._bot = bot

    @staticmethod
    def create_help(msg):
        """
        Generates the general help embed
        params: messages object (messages.json)
        returns: help menu embedded
        """
        embed = discord.Embed(title=msg.help_title,
                              description=msg.help_description,
                              color = discord.Colour.purple())
        embed.add_field(name=msg.source, value=msg.github)
        embed.set_footer(text=msg.help_footer)
        return embed

    @commands.command(name="link")
    async def get_github_link(self, ctx):
        """
        Send github channel to developers.
        params: message context object
        """
        await ctx.send(GITHUB_LINK)

    @commands.command(name="help")
    @commands.cooldown(1, RATE_COOLDOWN, commands.BucketType.user)
    async def get_help(self, ctx):
        """
        Sends general/specific manual for commands.
        params: context object (discord message)
        """
        command = ctx.message.content.split()

        # default help
        if len(command) == 1:
            embed = Meta.create_help(msg)
            await ctx.channel.send(embed=embed)

        # command specific help
        # WIP


def setup(bot):
        bot.add_cog(Meta(bot))
