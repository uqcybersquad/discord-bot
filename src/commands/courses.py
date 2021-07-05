import os
import discord

# https://github.com/ChaoticCooties/uq-scraper
from .uqscraper import UQScraper as uqscraper

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
RATE_COOLDOWN = os.getenv("RATE_COOLDOWN")


class Course:
    """
    Course information fetched from UQ website
    params: course code
    """

    def __init__(self, course_code: str):
        try:
            scraper = uqscraper(course_code)
        except ValueError:
            raise ValueError()

        self.url = scraper.get_url()
        self.title = scraper.get_title()
        self.level = scraper.get_level()
        self.prereq = scraper.get_prerequisite()
        self.rec_preq = scraper.get_recommended_prerequisite()
        self.assessment = scraper.get_assessment()
        self.summary = scraper.get_summary()
        self.summary = f"""
            **Summary**

            {self.summary}

            """
        self.coordinator = scraper.get_coordinator()


class Courses(commands.Cog):
    """
    Generate course information dynamically from the UQ website
    """

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_course_embed(course: Course):
        """
        Generates the course info embed message
        params: course object
        returns: embed object
        """
        embed = discord.Embed(
            title=course.title,
            description=course.summary,
            color=discord.Colour.purple(),
        )
        embed.add_field(name="Prerequisites", value=course.prereq)
        embed.add_field(name="Recommended", value=course.rec_preq)
        embed.add_field(name="Assessment", value=course.assessment)
        embed.add_field(name="Website", value=f"[Link]({course.url})")
        embed.set_footer(text=f"Coordinator: {course.coordinator}")
        return embed

    @commands.command(name="course")
    @commands.cooldown(1, RATE_COOLDOWN, commands.BucketType.user)
    async def get_course(self, ctx, course_code: str):
        """
        Sends course related information to Discord
        params: course code
        """
        try:
            course_data = Course(course_code)
            embed = Courses.create_course_embed(course_data)
            await ctx.channel.send(embed=embed)
        except ValueError:
            await ctx.channel.send(f'Error: "{course_code}" is not a valid course code')


def setup(bot):
    bot.add_cog(Courses(bot))
