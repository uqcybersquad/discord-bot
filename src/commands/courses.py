import discord
from discord.ext import commands


"""
Generate course information dynamically from the UQ website
"""
class Courses(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="course")
    async def get_course_info(self, ctx, c_name : str):
        await ctx.send("It's coming, trust...\n")

    #@commands.command(name="course")
    #async def funcname(self, ctx, c_name : str):
    #    pass


def setup(bot):
	bot.add_cog(Courses(bot))