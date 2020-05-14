import discord
from discord.ext import commands

import datetime

'''NOTE: given times are in UTC (most CTFs seem to be planned in it)'''
class Competitions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_time_diff(self, event_time, ending):
        now_time = datetime.datetime.now()

        waiting = event_time - now_time

        if waiting.seconds < 0:
            msg = "Uhhhhh, you may have missed it...\n"
        else:
            msg = f"There are {waiting.days} day(s), {waiting.seconds // (60 * 60) % 24} hour(s), {waiting.seconds // (60) % 60} minutes and {waiting.seconds % 60} second(s) {ending}\n"

        return msg
    
    @commands.command(name="hackasat")
    async def hackasat_command(self, ctx):

        event_time = datetime.datetime(year = 2020, month = 5, day = 23, hour = 0)

        msg = self.get_time_diff(event_time, "until launch!")

        await ctx.send(msg)

    @commands.command(name="sharkyctf")
    async def sharky_command(self, ctx):

        event_time = datetime.datetime(year = 2020, month = 5, day = 9, hour = 0)

        msg = self.get_time_diff(event_time, "until we need a bigger boat...")
        
        await ctx.send(msg)

    @commands.command(name="defcon")
    async def defcon_command(self, ctx):

        quals_time = datetime.datetime(year = 2020, month = 5, day = 16, hour = 0)
        finals_time = datetime.datetime(year = 2020, month = 8, day = 6, hour = 0)
        
        quals_msg = self.get_time_diff(quals_time, "until we get to qualify (or die of exhaustion in the process)")
        finals_msg = self.get_time_diff(finals_time, "until ~~nuclear~~ cyber armageddon")

        msg = quals_msg + finals_msg

        await ctx.send(msg)

    


def setup(bot):
	bot.add_cog(Competitions(bot))