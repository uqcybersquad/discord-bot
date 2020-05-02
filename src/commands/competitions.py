import discord
from discord.ext import commands

import datetime


class Competitions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hackasat_time = datetime.datetime(year = 2020, month = 5, day = 23, hour = 10)

    
    @commands.command(name="hackasat")
    async def hackasat_command(self, ctx):
        now_time = datetime.datetime.now()

        waiting = self.hackasat_time - now_time

        if waiting.seconds < 0:
            msg = "Uhhhhh, you may have missed it...\n"
        else:
            msg = f"There are {waiting.days} days, {waiting.seconds // (60 * 60) % 24} hours, {waiting.seconds // (60) % 60} minutes and {waiting.seconds % 60} seconds until launch!\n"
        
        await ctx.send(msg)

def setup(bot):
	bot.add_cog(Competitions(bot))