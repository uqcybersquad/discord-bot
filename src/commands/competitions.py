import discord
from discord.ext import commands

import datetime


class Competitions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_time_diff(self, event_time, ending):
        now_time = datetime.datetime.now()

        waiting = event_time - now_time

        if waiting.seconds < 0:
            msg = "Uhhhhh, you may have missed it...\n"
        else:
            msg = f"There are {waiting.days} days, {waiting.seconds // (60 * 60) % 24} hours, {waiting.seconds // (60) % 60} minutes and {waiting.seconds % 60} {ending}\n"

        return msg
    
    @commands.command(name="hackasat")
    async def hackasat_command(self, ctx):

        event_time = datetime.datetime(year = 2020, month = 5, day = 23, hour = 10)

        msg = self.get_time_diff(event_time, "until launch!")

        await ctx.send(msg)

    @commands.command(name="sharkyctf")
    async def sharky_command(self, ctx):

        event_time = datetime.datetime(year = 2020, month = 5, day = 9, hour = 10)

        msg = self.get_time_diff(event_time, "until we need a bigger boat...")
        
        await ctx.send(msg)

    


def setup(bot):
	bot.add_cog(Competitions(bot))