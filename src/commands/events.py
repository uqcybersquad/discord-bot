import discord
import messages

from discord.ext import tasks, commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import datetime
import dateparser

sched = AsyncIOScheduler()
sched.start()

msg =  messages.Messages()
react_emoji = '<:hacking:681070378516611097>'

class Reminder:
    """
    A reminder object scheduled to ping all users who reacted to the reminder.
    """
    def __init__(self, bot, ctx, sched_time, title: str, info: str):
        self.bot = bot
        self.ctx = ctx
        self.sched_time = sched_time
        self.title = title
        self.info = info
        self.current = datetime.datetime.now()
        self.reminder = None
        sched.add_job(self.send_reminder, 'date', run_date=sched_time)

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

            embed = discord.Embed(title=self.title,
                                  description=self.info,
                                  color= discord.Colour.purple())
            time_remaining = (f'{int(days[0])} days, {int(hours[0])} hours,'
                            f' {int(minutes[0])} minutes')
            embed.add_field(name='Event Time/Date',
                            value=self.sched_time.strftime('%c'))
            embed.add_field(name='Time remaining', value=time_remaining)
            embed.set_footer(text='React to this message to get notified when the event starts!')
            self.reminder = await self.ctx.send(embed=embed)
            await self.reminder.add_reaction(react_emoji)
            self.update_reminder.start()

    async def send_reminder(self):
        """
        Notifies all users and deletes the reminder once the
        countdown reaches zero.
        """
        # Get cached message for reactions iteration
        # Wonky API causes wonky code
        message = await self.bot.get_channel(self.reminder.channel.id).fetch_message(self.reminder.id)
        for reaction in message.reactions:
            if (str(reaction.emoji) == react_emoji):
                users = await reaction.users().flatten()
                users = " ".join([user.mention for user in users if not user.bot])
                await self.ctx.send(f'{self.title} has started! {users}')
                self.update_reminder.cancel()

    @tasks.loop(minutes=1.0)
    async def update_reminder(self):
        # Calculate the remaining time 
        time_length = (self.sched_time - datetime.datetime.now()).total_seconds()
        days    = divmod(time_length, 86400)
        hours   = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        time_remaining = (f'{int(days[0])} days, {int(hours[0])} hours,'
                        f' {int(minutes[0])} minutes')

        # Update time remaining field
        message = await self.bot.get_channel(self.reminder.channel.id).fetch_message(self.reminder.id)
        embed = message.embeds[0]
        embed.set_field_at(1, name='Time remaining', value=time_remaining)
        await message.edit(embed=embed)


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
        Command format: '!event [time]|[event name]|[event_info]'
        """
        await ctx.message.delete()
        args = ctx.message.content.split()
        args = " ".join(args[1:])
        time, event, event_info = args.split('|')

        parsed_time = dateparser.parse(time)
        print(f'Parsed Time: {parsed_time}')
        print(f'Current Time: {datetime.datetime.now()}')
        if parsed_time is None or event is None:
            await ctx.send(msg.err_parse)
        else:
            reminder = Reminder(self.bot, ctx, parsed_time, event, event_info)
            await reminder.set_reminder()


def setup(bot):
	bot.add_cog(Events(bot))
