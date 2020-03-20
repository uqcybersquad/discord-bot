import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
	    self.bot = bot

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
	    self.bot.load_extension(f'commands.{extension}')

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
	    self.bot.unload_extension(f'commands.{extension}')

    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discrimination) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return

def setup(bot):
    bot.add_cog(Admin(bot))
