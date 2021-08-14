import discord
import DiscordUtils
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed1 = discord.Embed(color = ctx.author.color).add_field(title = "User commands", value = "Nothing to see here")
        embed2 = discord.Embed(color = ctx.author.color).add_field(title = "Admin commands", value = "-admin ban \n -admin unban \n -admin kick \n -admin mute \n -admin unmute")
        embed3 = discord.Embed(color = ctx.author.color).add_field(title = "Economic commands", value = "Nothing to see here")
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions = True)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3]
        await paginator.run(embeds)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
    print("Help command extension successfully registered")