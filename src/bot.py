import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import base64


load_dotenv()

API_KEY = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_GUILD')

mrRobot = commands.Bot(command_prefix='!')


@mrRobot.event
async def on_ready():

	guild = mrRobot.guilds[0]
	memberCount = len(guild.members)
	onlineMemberCount = len([mem for mem in guild.members if mem.status == discord.Status.online])

	print(f'{mrRobot.user} is connected to: ' + f'{guild.name}')
	print(f'There are {onlineMemberCount} of {memberCount} people online!')



@mrRobot.command(name='base64')
async def base64_enc_dec(ctx, opt : str, msg = ""):
	helpMsg = "You're using me wrong :(\nUsage: base64 -[e/d] message\n-d\t\tdecode\n-e\t\tencode\n"

	if opt in ["-e", "-d"] and msg != "":
		# Correct method request
		if opt == "-e":
			encoded = base64.b64encode(msg.encode('ascii'))
			
			response = encoded.decode("utf-8")
			print(response)

		elif opt == "-d":
			decoded = base64.b64decode(msg.encode('ascii'))

			response = decoded.decode("utf-8")

	elif opt not in ["-e", "-d"] and msg == "":
		# Default decode
		decoded = base64.b64decode(opt.encode('ascii'))

		response = decoded.decode("utf-8")
	else:
		# Incorrect usage
		response = helpMsg


	await ctx.send(response)


@mrRobot.command(name='test')
async def test_command(ctx):
	response = "This is a test message. :hellothere:"

	await ctx.send(response)


mrRobot.run(API_KEY)