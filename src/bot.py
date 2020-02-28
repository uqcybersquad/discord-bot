import os

import discord
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():

	guild = client.guilds[0]

	print(f'{client.user} is connected to: ' + f'{guild.name}')


	members = '\n - '.join([member.name for member in guild.members])

	print(f'Members:\n - {members}')


client.run(API_KEY)