import os
import discord
import requests
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

import datetime
from dateutil import tz, parser

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

load_dotenv()
RATE_COOLDOWN = os.getenv("RATE_COOLDOWN")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CTF_CALENDAR = "i73qh029nqq8n4ah6oltt7pmvs@group.calendar.google.com"


class CTF(commands.Cog):
    """
    Fetch CTF information
    """

    def __init__(self, bot):
        self.bot = bot
        self.creds = None
        # Thself.e file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    @staticmethod
    def convert_time(time):
        """
        Parses the time, converts it to Australia/Brisbane, and returns the
        printable output.
        params: ISO 8601 time
        returns: Brisbane locale time
        """
        aus_tz = tz.gettz("Australia/Brisbane")
        parsed_time = parser.isoparse(time)
        converted_time = parsed_time.astimezone(aus_tz).strftime("%a %d %b %H:%M")
        return converted_time

    @staticmethod
    def build_ctf_list(events, curr_page=0):
        """
        Builds an embed of upcoming ctfs
        params: events json
        returns: list of embeds
        """

        def strfdelta(tdelta, fmt):
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            return fmt.format(**d)

        num_pages = len(events) // 5
        if len(events) % 5 > 0:
            num_pages += 1

        embed = discord.Embed(
            title=f"Upcoming CTFs {curr_page + 1}/{num_pages}",
            color=discord.Colour.purple(),
        )

        start_idx = curr_page * 5
        end_idx = (num_pages - 1) * 5 + 1
        for event in events[start_idx:end_idx]:
            start = CTF.convert_time(event["start"]["dateTime"])
            finish = CTF.convert_time(event["end"]["dateTime"])
            time_remaining = parser.isoparse(
                event["start"]["dateTime"]
            ) - datetime.datetime.now(tz.gettz("Australia/Brisbane"))
            time_remaining = strfdelta(
                time_remaining,
                "{days} days {hours} \
                                       hours and {minutes} minutes",
            )

            title = event["summary"]
            link = event["description"] if "description" in event else ""
            desc = f"""
                **Time Remaining**: {time_remaining}
                **Start**: {start} UTC+10
                **Finish**: {finish} UTC+10
                **Description**: {link}
            """
            embed.add_field(name=title, value=desc, inline=False)
        return num_pages, embed

    @commands.command(name="lsctf")
    @commands.cooldown(1, RATE_COOLDOWN, commands.BucketType.guild)
    async def list_ctf_events(self, ctx):
        """
        List of upcoming CTFs in UQCS Google Calendar
        returns: msg response listing upcoming CTFs
        """

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["\u25c0", "\u25b6"]

        # 'Z' indicates UTC time
        now = datetime.datetime.utcnow().isoformat() + "Z"
        service = build("calendar", "v3", credentials=self.creds)
        events = (
            service.events()
            .list(
                calendarId=CTF_CALENDAR,
                timeMin=now,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        num_pages, embed = CTF.build_ctf_list(events["items"])
        message = await ctx.send(embed=embed)

        # Multipage handler
        await message.add_reaction("\u25c0")  # <
        await message.add_reaction("\u25b6")  # >

        curr_page = 0
        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60, check=check
                )
                if str(reaction.emoji) == "\u25c0" and curr_page > 0:
                    curr_page -= 1
                elif str(reaction.emoji) == "\u25b6" and curr_page != num_pages:
                    curr_page += 1

                # Rebuild the embed and update message with new embed
                new_embed = CTF.build_ctf_list(events, curr_page)
                await message.edit(embed=new_embed)
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @commands.command(name="register")
    @commands.cooldown(1, RATE_COOLDOWN, commands.BucketType.user)
    async def create_ctf_lobby(self, ctx, *args):
        """
        Creates a new category, channel, and a new role
        for an upcoming CTF.
        """
        ctf_name = " ".join(args)
        guild = ctx.guild
        role = await guild.create_role(name=ctf_name, reason="CTF Registration")
        category = await guild.create_category(
            name=ctf_name, reason="CTF Registration", position=2
        )

        # Creates read/write perms for new role only
        role_perms = category.overwrites_for(role)
        role_perms.read_messages = True
        role_perms.send_messages = True
        guest_perms = category.overwrites_for(ctx.guild.default_role)
        guest_perms.read_messages = False

        await category.set_permissions(role, overwrite=role_perms)
        await category.set_permissions(ctx.guild.default_role, overwrite=guest_perms)
        channel = await category.create_text_channel(
            ctf_name, reason="CTF Registration"
        )
        return channel


def setup(bot):
    bot.add_cog(CTF(bot))
