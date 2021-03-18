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
    def __init__(self, bot, sched_time, title: str, info: str):
        self.bot = bot
        self.title = title
        self.info = info
        self.complete = False
        self.message = None
        self.sched_time = sched_time
        sched.add_job(self.trigger_notify, 'date', run_date=sched_time)

    async def send_reminder(self, ctx):
        """
        Sends a reminder in the discord channel.
        Sends an embed message containing the details.
        """
        time_length = (self.sched_time - datetime.datetime.now()).total_seconds()
        if time_length < 0:
            await ctx.send('Error: Provided time has already passed.')
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
            self.message = await ctx.send(embed=embed)
            await self.message.add_reaction(react_emoji)

    async def trigger_notify(self):
        """
        Notifies all users who reacted to the post when the reminder/event has started.
        """
        # Tells the scheduler that the reminder has been fulfilled.
        self.complete = True
        # Get cached message for reactions iteration
        message = await self.bot.get_channel(self.message.channel.id).fetch_message(self.message.id)
        if message is None:
            self.complete = True
            raise TypeError('Message could not be found. NoneType was returned.')

        for reaction in message.reactions:
            if (str(reaction.emoji) == react_emoji):
                users = await reaction.users().flatten()
                users = " ".join([user.mention for user in users if not user.bot])
                ctx = await self.bot.get_context(message)
                await ctx.send(f'{self.title} has started! {users}')

    async def update_reminder(self):
        # Calculate the remaining time 
        time_length = (self.sched_time - datetime.datetime.now()).total_seconds()
        days    = divmod(time_length, 86400)
        hours   = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        time_remaining = (f'{int(days[0])} days, {int(hours[0])} hours,'
                        f' {int(minutes[0])} minutes')

        # Update time remaining field
        message = await self.bot.get_channel(self.message.channel.id).fetch_message(self.message.id)
        if message is None:
            self.complete = True

        # Update time remaining
        embed = message.embeds[0]
        embed.set_field_at(1, name='Time remaining', value=time_remaining)
        await message.edit(embed=embed)

class ReminderScheduler:
    """
    Handles Reminder objects and concurrently tracks them for update
    """
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}
        # Start task 
        self.update_reminders.start()

    async def add_reminder(self, ctx, sched_time, title: str, desc: str):
        """
        Adds a Reminder in discord. Also adds it to the list for tracking.
        """
        reminder = Reminder(self.bot, sched_time, title, desc)
        await reminder.send_reminder(ctx)
        self.reminders[title] = reminder

    @tasks.loop(minutes=1.0, reconnect=True)
    async def update_reminders(self):
        """
        Update list of reminders being tracked (time etc)
        Removes reminder from scheduler if the scheduled time has passed
        """
        # Get a copy of the reminders dict to prevent runtime modifying error
        for reminder in self.reminders.copy().values():
            # Remove from tracking if sched time has passed
            print(f'TEST TEST TEST {reminder}')
            if reminder.complete:
                self.reminders.pop(reminder.title)
                print(f'Log: Removed {reminder.title} from scheduler')
            else:
                await reminder.update_reminder()

    async def remove_reminder(self, ctx, title: str):
        """
        Removes a Reminder in discord. Also removes it from the scheduler.
        """
        # Remove embed message reminder
        old_message = self.reminders[title].message
        message = await self.bot.get_channel(old_message.channel.id).fetch_message(old_message.id)
        await message.delete()
        try:
            self.reminders.pop(title)
            await ctx.send('Cancelled reminder')
        except KeyError:
            await ctx.send('Title not found')

class Events(commands.Cog):
    """
    Allows Mods/Admins to schedule events. Particularly useful for CTFs
    or live meetups
    """
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = ReminderScheduler(self.bot)

    @commands.command(name='remind')
    @commands.has_any_role('Board', 'Mod')
    async def add_event(self, ctx):
        """
        Adds a new event
        Command format: '!event [time]|[event name]|[event_info]'
        """
        # await ctx.message.delete()
        try:
            args = ctx.message.content.split()
            args = " ".join(args[1:])
            time, event, event_info = [x.strip() for x in args.split('|')]
        except:
            await ctx.send(msg.err_parse)

        parsed_time = dateparser.parse(time, settings={'DATE_ORDER': 'DMY'})
        await self.scheduler.add_reminder(ctx, parsed_time, event, event_info)

    @commands.command(name='rmremind')
    @commands.has_any_role('Board', 'Mod')
    async def remove_event(self, ctx, title: str):
        """
        Removes an event
        Command format: '!rmremind [event title]'
        """
        await self.scheduler.remove_reminder(ctx, title)

def setup(bot):
	bot.add_cog(Events(bot))
