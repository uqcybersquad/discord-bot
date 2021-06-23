import os
import discord
import requests
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

import dateparser
from dateutil import tz

load_dotenv()
RATE_COOLDOWN = os.getenv('RATE_COOLDOWN')

class CTF(commands.Cog):
    """
    Fetch CTF information
    """
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://ctftime.org/api/v1/events/?limit=20"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }

    @staticmethod
    def convert_time(time):
        """
        Parses the time, converts it to Australia/Brisbane, and returns the
        printable output.
        params: UTC time string
        returns: Brisbane locale time
        """
        aus_tz = tz.gettz('Australia/Brisbane')
        parsed_time = dateparser.parse(time)
        converted_time = parsed_time.astimezone(aus_tz).strftime("%a %d %b %H:%M")
        return converted_time

    @staticmethod
    def build_ctf_list(events, curr_page=0):
        """
        Builds an embed of upcoming ctfs
        params: events json
        returns: ctf list embed
        """
        embed = discord.Embed(title=f'Upcoming CTFs {curr_page + 1}/4',
                              color=discord.Colour.purple())
        embed.set_footer(text='Brisbane UTC+10')
        idx = curr_page * 5

        for i in range(idx, idx + 5):
            title = events[i]['title']
            start = CTF.convert_time(events[i]['start'])
            finish = CTF.convert_time(events[i]['finish'])
            link = events[i]['url']
            desc = f'''
                **Start**: {start}
                **Finish**: {finish}
                **Link**: [{link}]({link})

            '''
            embed.add_field(name=title, value=desc, inline=False)
        return embed

    @commands.command(name="ctfs")
    @commands.cooldown(1, RATE_COOLDOWN, commands.BucketType.user)
    async def list_ctfs(self, ctx):
        """
        List of CTFs from ctftime.org, multi-page for easier navigation
        TODO: Allow custom entries
        returns: ctf list
        """
        # Fetch from ctftime.org
        r = requests.get(self.url, headers=self.headers)
        events = r.json()

        # Build embed
        tot_page = 3
        curr_page = 0
        embed = CTF.build_ctf_list(events)
        message = await ctx.send(embed=embed)

        # Multipage handler
        await message.add_reaction("\u25c0") # < 
        await message.add_reaction("\u25b6") # >
        def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["\u25c0",
                                                                      "\u25b6"]
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=45,
                                                   check=check)
                if str(reaction.emoji) == '\u25c0' and curr_page > 0:
                    curr_page -= 1
                elif str(reaction.emoji) == '\u25b6' and curr_page != tot_page:
                    curr_page += 1

                # Rebuild the embed and update message with new embed
                new_embed = CTF.build_ctf_list(events, curr_page)
                await message.edit(embed=new_embed)
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

def setup(bot):
	bot.add_cog(CTF(bot))
