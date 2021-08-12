import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        await ctx.send("Test")

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
    print("Help command extension successfully registered")