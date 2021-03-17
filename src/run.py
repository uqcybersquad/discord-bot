import os

from dotenv import load_dotenv

import discord
from discord.ext import commands

# Get environment variables
load_dotenv()
API_KEY = os.getenv('DISCORD_TOKEN')
SERVER_NAME = os.getenv('DISCORD_GUILD')

# List of modules
initial_modules = ['meta', 'courses', 'events', 'board']

bot = commands.Bot(
	command_prefix='!',
	activity=discord.Game(name="!help"),
        help_command=None
)

@bot.event
async def on_ready():
        print(
            f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
        print('Use this link to invite {}:'.format(bot.user.name))
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))

# Embedded Message
def embed(title, desc, color):
    color = discord.Color(int(color, 16))
    embed = discord.Embed(title=title, color=color)
    embed.description = desc
    return embed

@bot.command(name='embed')
async def embedmsg(ctx, title, msg, color):
    await ctx.message.delete()
    embed_msg = embed(title, msg, color)
    await ctx.message.channel.send(embed=embed_msg)

# Load modules listed in initial_modules
if __name__ == '__main__':
    for module in initial_modules:
        try:
            bot.load_extension(f"commands.{module}")
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load module {}\n{}'.format(module, exc))

# Runs and automatically reconnects if connection is aborted.
bot.run(API_KEY, reconnect="True")
