import discord
from discord.ext import commands, tasks
import random

quotes = ['I believe in fate. There’s a reason we met. There’s something between us. I can see it.',
			'She doesn’t love the people who love her. She loves the people who don’t.',
			'Give a man a gun and he can rob a bank, but give a man a bank, and he can rob the world.',
			"You’re never sure about anything unless there’s something to be sure about.",
			"When you see a good move, look for a better one.",
			"People always told me growing up that it’s never about the destination. It’s about the journey. But what if the destination is you?",
			"A bug is never just a mistake. It represents something bigger. An error of thinking that makes you who you are.",
			"Don’t mistake my generosity for generosity.",
			"I’m good at reading people. My secret , I look for the worst in them.",
			"The concept of waiting bewilders me. There are always deadlines. There are always ticking clocks.",
			"I never want to be right about my hacks, but people always find a way to disappoint.",
			"Most kids get scared shitless when they’re alone, but I wasn’t. I loved it.",
			"Getting into the mind of a woman, it’s the toughest route for even the best sources.",
			"Though she’s a psychologist she’s really bad at reading people but I’m good at reading people. My secret? I look for the worst in them.",
			"Unfortunately, we’re all human. Except me, of course.",
			"Control can sometimes be an illusion. But sometimes you need illusion to gain control.",
			"I’ve never found it hard to hack most people. If you listen to them, watch them, their vulnerabilities are like a neon sign.",
			"When we lose our principles, we invite chaos."]

class Quotes(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.send_quote.start()

	@commands.command(name='quote')
	async def random_quote(self, ctx):
		await ctx.send(random.choice(quotes))

	@tasks.loop(seconds=1800)
	async def send_quote(self):
		#print(next(quotes))
		channel_id = self.client.get_channel(687098371944874148)
		await channel_id.send(random.choice(quotes))
	#@commands.command()
	#async def ping(self, ctx):
	#	await ctx.send("Pong");

def setup(client):
	client.add_cog(Quotes(client))
