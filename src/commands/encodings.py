import discord
from discord.ext import commands

import base64

class Encodings(commands.Cog):
	def __init__(self, client):
	    self.client = client

	@commands.command(name='base64')
	async def base64_enc_dec(ctx, opt : str, msg = ""):
		helpMsg = "You're using me wrong :(\nUsage: base64 -[e/d] message\n-d\t\tdecode\n-e\t\tencode\n"

		if opt in ["-e", "-d"] and msg != "":
			# Correct method request
			if opt == "-e":
				encoded = base64.b64encode(msg.encode('ascii'))
				
				response = encoded.decode("utf-8")
				print(response)

			elif opt == "-d":
				decoded = base64.b64decode(msg.encode('ascii'))

				response = decoded.decode("utf-8")

		elif opt not in ["-e", "-d"] and msg == "":
			# Default decode
			decoded = base64.b64decode(opt.encode('ascii'))

			response = decoded.decode("utf-8")
		else:
			# Incorrect usage
			response = helpMsg


		await ctx.send(response)
		
		
def setup(client):
	client.add_cog(Encodings(client))