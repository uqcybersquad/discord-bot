import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

from ciphey import decrypt
from ciphey.iface import Config


load_dotenv()
RATE_COOLDOWN = os.getenv('RATE_COOLDOWN')

class Encodings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
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
    """

    @commands.command(name='lolcrypto')
    @commands.cooldown(1, RATE_COOLDOWN, commands.BucketType.user)
    async def lolcrypto(self, ctx, enc_string: str):
        res = "hello"
        print(res)


def setup(bot):
	bot.add_cog(Encodings(bot))
