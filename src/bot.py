import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import base64


load_dotenv()

API_KEY = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_GUILD')

#client = discord.Client()
mrRobot = commands.Bot(command_prefix='!')

"""
@client.event
async def on_ready():

	guild = client.guilds[0]

	print(f'{client.user} is connected to: ' + f'{guild.name}')"""

@mrRobot.command(name='base64')
async def base64_enc_dec(ctx, opt : str, msg : str):
	helpMsg = "You're using me wrong :(\nUsage: base64 -[e/d] message\n-d    - decode\n-e    - encode\n"

	if msg is None:
		response = helpMsg

	if opt == "-e":
		encoded = base64.b64encode(msg.encode('ascii'))
		
		response = encoded.decode("utf-8")
		print(response)

	elif opt == "-d" or opt is None:
		decoded = base64.b64decode(msg.encode('ascii'))

		response = decoded.decode("utf-8")

	else:
		response = helpMsg

	await ctx.send(response)


@mrRobot.command(name='test')
async def test_command(ctx):
	response = "This is a test message. :hellothere:"

	await ctx.send(response)


#client.run(API_KEY)
mrRobot.run(API_KEY)