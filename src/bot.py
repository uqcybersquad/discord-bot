import os

import discord
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_GUILD')

client = discord.Client()

print("API key is: " + os.getenv('DISCORD_TOKEN'))

@client.event
async def on_ready():
	for i,guild in enumerate(client.guilds):
		print("No:" + str(i) + "is: " + guild.name)
		if guild.name == SERVER_NAME:
			break


	print(f'{client.user} is connected to guild:' + f'{guild.name}')


client.run(API_KEY)