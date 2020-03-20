import os
import base64

from dotenv import load_dotenv

import discord
from discord.ext import commands




load_dotenv()

API_KEY = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_GUILD')


mrRobot = commands.Bot(
	command_prefix='!',
	activity=discord.Game(name="Commands: !help"),
)


@mrRobot.event
async def on_ready():

	guild = mrRobot.guilds[0]
	memberCount = len(guild.members)
	onlineMemberCount = len([mem for mem in guild.members if mem.status == discord.Status.online])

	print(f'{mrRobot.user} is connected to: {guild.name}')
	print(f'There are {onlineMemberCount} of {memberCount} people online!')

	modules = [
		"admin",
		"encodings",
		"quotes",	
	]

	for mod in modules:
		mrRobot.load_extension(f"commands.{mod}")


mrRobot.run(API_KEY)
