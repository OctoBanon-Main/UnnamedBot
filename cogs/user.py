import sqlite3
import discord
import datetime
from discord.ext import commands

con = sqlite3.connect("database.db")
cur = con.cursor()

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def warns(self, ctx):
        warns_msg = cur.execute("SELECT warns FROM warns WHERE user_id = ? AND guild_id = ?", (ctx.message.author.id, ctx.message.guild.id,)).fetchone()
        WarnsEmbed = discord.Embed(
            title = "Your warns",
            description = "#",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        WarnsEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        WarnsEmbed.add_field(name = "Warns: ", value = f"{warns_msg[0]}")
        await ctx.send(embed=WarnsEmbed)

def setup(bot):
    bot.add_cog(User(bot))
    print("User commands extension successfully registered")
