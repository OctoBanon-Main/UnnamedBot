import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def kick(self, ctx, member:discord.Member, *, reason = None):
        if reason is None:
            reason="Not specified"
        
        await member.kick(reason=reason)
        await ctx.send(f"Member **{member.display_name}** has been successfully kicked from the server with reason: **{reason}**")

    @commands.command()
    async def mute(self, ctx, member:discord.Member, *, reason = None):
        role = discord.utils.get(member.guild.roles, name="Muted")
        if reason is None:
            reason="Not specified"
        await member.add_roles(role)
        await ctx.send(f"Member **{member.display_name}** has been successfully muted on the server with reason: **{reason}**")

    @commands.command()
    async def unmute(self, ctx, member:discord.Member):
        role = discord.utils.get(member.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f"Member **{member.display_name}** has been successfully unmuted on the server")


def setup(bot):
    bot.add_cog(Admin(bot))
    print("Admin commands extension successfully registered")