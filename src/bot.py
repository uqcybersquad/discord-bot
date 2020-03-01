import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_GUILD')

client = discord.Client()
mrRobot = commands.Bot(command_prefix="!")

"""
@client.event
async def on_ready():

	guild = client.guilds[0]

	print(f'{client.user} is connected to: ' + f'{guild.name}')"""


@mrRobot.command(name="test")
async def test_command(ctx):
	response = "This is a test message. :hellothere:"

	await ctx.send(response)


client.run(API_KEY)