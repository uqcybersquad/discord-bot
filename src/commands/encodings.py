import discord
from discord.ext import commands

import base64
import string

class Encodings(commands.Cog):
	def __init__(self, bot):
	    self.bot = bot

	@commands.command(name="base64")
	async def base64_enc_dec(self, ctx, opt : str, msg = ""):
		helpMsg = "You're using me wrong :(\nUsage: base64 -[e/d] message\n-d\t\tdecode\n-e\t\tencode\n"

		if opt in ["-e", "-d"] and msg != "":
			# Correct method request
			if opt == "-e":
				encoded = base64.b64encode(msg.encode('ascii'))

				try:
					response = encoded.decode("utf-8")
				except:
					response = helpMsg

			elif opt == "-d":
				decoded = base64.b64decode(msg.encode('ascii'))

				try:
					response = decoded.decode("utf-8")
				except:
					response = helpMsg

		elif opt not in ["-e", "-d"] and msg == "":
			# Default decode
			decoded = base64.b64decode(opt.encode('ascii'))

			try:
				response = decoded.decode("utf-8")
			except:
				response = helpMsg
		else:
			# Incorrect usage
			response = helpMsg


		await ctx.send(response)

	@commands.command(name="rot13")
	async def rot13_cipher(self, ctx, msg = ""):
		helpMsg = "Usage: rot13 message\n"

		if not msg:
			ctx.send(helpMsg)
		else:
			response = ""

			for letter in msg:

				if letter not in string.ascii_letters:
					response += letter
					continue

				if letter == letter.toLower():
					index = string.ascii_lowercase.index(letter)
					response += string.ascii_lowercase[index % 26]
				else:
					index = string.ascii_uppercase.index(letter)
					response += string.ascii_uppercase[index % 26]
			
			ctx.send(response)
				



def setup(bot):
	bot.add_cog(Encodings(bot))
