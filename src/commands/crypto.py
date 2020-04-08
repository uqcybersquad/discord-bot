import discord
from discord.ext import commands

import base64
import string
from itertools import cycle
import binascii

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
		helpMsg = "Usage: rot13 [message]\n"

		if not msg:
			response = helpMsg
			await ctx.send(response)
		else:
			await self.rotn_cipher(ctx, 13, msg)


	@commands.command(name="rot")
	async def rotn_cipher(self, ctx, n, msg = ""):
		helpMsg = "Usage: rot [rotations] [message]\n"
		n = int(n)

		if not msg or n not in range(-27,27):
			response = helpMsg
		else:
			response = ""

			for letter in msg:

				if letter not in string.ascii_letters:
					response += letter
					continue

				if letter.islower():
					index = string.ascii_lowercase.index(letter)
					response += string.ascii_lowercase[(index + n)  % 26]
				else:
					index = string.ascii_uppercase.index(letter)
					response += string.ascii_uppercase[(index + n) % 26]
			
		await ctx.send(response)


	@commands.command(name="xor")
	async def xor_cipher(self, ctx, key="", msg=""):
		helpMsg = "Usage: xor [key] [message]\n"
		response = ""

		if not msg or not key:
			response = helpMsg
		else:
			decoded = ''.join(chr(ord(let) ^ ord(k)) for (let, k) in zip(msg, cycle(key)))
			response = "str: {}\nhex: {}\n".format(decoded, binascii.hexlify(decoded.encode('utf8')).decode())

		await ctx.send(response)


def setup(bot):
	bot.add_cog(Encodings(bot))
