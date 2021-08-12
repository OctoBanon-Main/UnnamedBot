import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        # Unknown command
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Unknown command")
        # Missing permissions
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permission to run this command!")
        # Input error
        elif isinstance(error, commands.UserInputError):
            await ctx.send("Something wrong happen in your input, please check your input and try again!")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    print("Error handler successfully registered")