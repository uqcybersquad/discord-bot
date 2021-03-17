import discord
import messages

from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import datetime
import dateparser

sched = AsyncIOScheduler()
sched.start()
msg =  messages.Messages()

class Reminder:
    """
    A reminder object scheduled to ping all users who reacted to the reminder.
    """
    def __init__(self, sched_time, ctx, msg: str):
        self.sched_time = sched_time
        self.ctx = ctx
        self.msg = msg
        self.current = datetime.datetime.now()

    async def set_reminder(self):
        """
        Sets a reminder in the discord channel.
        Sends an embed message containing the details.
        """
        time_length = (self.sched_time - datetime.datetime.now()).total_seconds()
        if time_length < 0:
            await self.ctx.send('Error: Provided time has already passed.')
        else:
            # Calculate the remaining time 
            days    = divmod(time_length, 86400)
            hours   = divmod(days[1], 3600)
            minutes = divmod(hours[1], 60)
            seconds = divmod(minutes[1], 1)

            embed = discord.Embed(title='Upcoming Event',
                                  description=self.msg,
                                  color= discord.Colour.purple())
            time_remaining = (f'{int(days[0])} days, {int(hours[0])} hours,'
                            f' {int(minutes[0])} minutes, {int(seconds[0])} seconds')
            embed.add_field(name='Time remaining', value=time_remaining)
            embed.set_footer(text='React to this message to get notified when the event starts!')
            reminder = await self.ctx.send(embed=embed)
            hacking = '<:hacking:681070378516611097>'
            await reminder.add_reaction(hacking)

    async def send_reminder(self):
        """

        """
        print('remind')


class Events(commands.Cog):
    """
    Allows Mods/Admins to schedule events. Particularly useful for CTFs
    or live meetups
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='remind')
    @commands.has_any_role('Board', 'Mod')
    async def add_event(self, ctx):
        """
        Adds a new event
        Command format: '!event [time]|[event]'
        """
        await ctx.message.delete()
        args = ctx.message.content.split()
        args = " ".join(args[1:])
        time, event = args.split('|')
        print(f'Time: {time}')
        print(f'Event: {event}')

        parsed_time = dateparser.parse(time)
        if parsed_time is None or event is None:
            await ctx.send(msg.err_parse)
        else:
            reminder = Reminder(parsed_time, ctx, event)
            await reminder.set_reminder()


def setup(bot):
	bot.add_cog(Events(bot))
