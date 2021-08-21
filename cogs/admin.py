import discord, sqlite3, datetime
from discord.ext import commands

con = sqlite3.connect("database.db")
cur = con.cursor()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member:discord.User, *, reason = None):
        if reason is None:
            reason = "Not specified"
        
        KickEmbed = discord.Embed(
            title = "Member kicked",
            description = "Member has been successfully kicked from the server!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        KickEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        KickEmbed.set_thumbnail(url = f"{member.avatar_url}")
        KickEmbed.add_field(name = "Kicked member: ", value = f"{member.mention}")
        KickEmbed.add_field(name = "Moderator: ", value = f"{ctx.message.author.mention}")
        KickEmbed.add_field(name = "Reason: ", value = f"**{reason}**")

        await ctx.message.delete()
        await member.kick(reason = reason)
        await ctx.send(embed = KickEmbed)
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member:discord.User, *, reason = None):
        if reason is None:
            reason = "Not specified"
        
        BanEmbed = discord.Embed(
            title = "Member banned",
            description = "Member has been successfully banned from the server!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        BanEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        BanEmbed.set_thumbnail(url = f"{member.avatar_url}")
        BanEmbed.add_field(name = "Banned member: ", value = f"{member.mention}")
        BanEmbed.add_field(name = "Moderator: ", value = f"{ctx.message.author.mention}")
        BanEmbed.add_field(name = "Reason: ", value = f"**{reason}**")

        await ctx.message.delete()
        await member.ban(reason = reason)
        await ctx.send(embed = BanEmbed)
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member:discord.User):
        user = discord.Object(id = member.id)
        
        UnbanEmbed = discord.Embed(
            title = "Member unbanned",
            description = "Member has been successfully unbanned on the server!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        UnbanEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        UnbanEmbed.set_thumbnail(url = f"{member.avatar_url}")
        UnbanEmbed.add_field(name = "Unbanned member: ", value = f"{member.mention}")
        UnbanEmbed.add_field(name = "Moderator: ", value = f"{ctx.message.author.mention}")

        await ctx.message.delete()
        await ctx.guild.unban(user)
        await ctx.send(embed=UnbanEmbed)

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member:discord.User, *, reason = None):
        if reason is None:
            reason = "Not specified"

        role = discord.utils.get(member.guild.roles, name = "Muted")

        MuteEmbed = discord.Embed(
            title = "Member muted",
            description = "Member has been successfully muted on the server!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        MuteEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        MuteEmbed.set_thumbnail(url = f"{member.avatar_url}")
        MuteEmbed.add_field(name = "Muted member: ", value = f"{member.mention}")
        MuteEmbed.add_field(name = "Moderator: ", value = f"{ctx.message.author.mention}")
        MuteEmbed.add_field(name = "Reason: ", value = f"**{reason}**")

        await ctx.message.delete()
        await member.add_roles(role)
        await ctx.send(embed = MuteEmbed)

    @commands.command()
    @commands.has_permissions(manage_roles = True)    
    async def unmute(self, ctx, member:discord.User):
        role = discord.utils.get(member.guild.roles, name = "Muted")

        UnmuteEmbed = discord.Embed(
            title = "Member unmuted",
            description = "Member has been successfully unmuted on the server!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        UnmuteEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        UnmuteEmbed.set_thumbnail(url = f"{member.avatar_url}")
        UnmuteEmbed.add_field(name = "Unmuted member: ", value = f"{member.mention}")
        UnmuteEmbed.add_field(name = "Moderator: ", value = f"{ctx.message.author.mention}")

        await ctx.message.delete()
        await member.remove_roles(role)
        await ctx.send(embed = UnmuteEmbed)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, ammout: int):
        ClearEmbed = discord.Embed(
            title = "Cleaning complete",
            description = "Channel has been successfully cleared!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        ClearEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        ClearEmbed.add_field(name = "Deleted messages: ", value = f"{ammout}")
        ClearEmbed.add_field(name = "In channel: ", value = f"{ctx.channel.mention}")
        ClearEmbed.add_field(name = "Moderator started cleaning: ", value = f"{ctx.message.author.mention}")

        await ctx.message.delete()
        await ctx.channel.purge(limit = ammout)
        await ctx.send(embed = ClearEmbed)
        
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def warn(self, ctx, member: discord.User, *, reason = None):
        if reason is None:
            reason = "Not specified"
        
        guild_id = ctx.message.guild.id
        warns = cur.execute("SELECT warns FROM warns WHERE user_id = ? AND guild_id = ?", (member.id, guild_id,)).fetchone()
                
        if cur.execute("SELECT user_id FROM warns WHERE user_id = ? AND guild_id = ?", (member.id, guild_id,)).fetchone() is None:
            cur.execute("INSERT INTO warns VALUES(?, ?, ?)", (member.id, guild_id, 1))
            con.commit()
        else:
            cur.execute("UPDATE warns SET warns = ? WHERE user_id = ? AND guild_id = ?", (warns[0]+1, member.id, guild_id,))
            con.commit()
        
        warns_msg = cur.execute("SELECT warns FROM warns WHERE user_id = ? AND guild_id = ?", (member.id, guild_id,)).fetchone()
        
        WarnEmbed = discord.Embed(
            title = "User warned",
            description = "Member has been successfully warned on the server!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        WarnEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        WarnEmbed.add_field(name = "Warned user: ", value = f"{member.mention}")
        WarnEmbed.add_field(name = "Moderator: ", value = f"{ctx.message.author.mention}")
        WarnEmbed.add_field(name = "Reason: ", value = f"**{reason}**")
        WarnEmbed.add_field(name = "Warns: ", value = f"{warns_msg[0]}")
        
        await ctx.message.delete()
        await ctx.send(embed = WarnEmbed)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unwarn(self, ctx, member: discord.User):
        guild_id = ctx.message.guild.id
        warns = cur.execute("SELECT warns FROM warns WHERE user_id = ? AND guild_id = ?", (member.id, guild_id,)).fetchone()

        if warns[0] < 1:
            await ctx.send("U can't xd")
            return 0

        if cur.execute("SELECT user_id FROM warns WHERE user_id = ? AND guild_id = ?", (member.id, guild_id,)).fetchone() is None:
            cur.execute("INSERT INTO warns VALUES(?, ?, ?)", (member.id, guild_id, 1))
            con.commit()
        else:
            cur.execute("UPDATE warns SET warns = ? WHERE user_id = ? AND guild_id = ?", (warns[0]-1, member.id, guild_id,))
            con.commit()
        
        WarnEmbed = discord.Embed(
            title = "User unwarned",
            description = "Member has been successfully unwarned on the server!",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        WarnEmbed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")
        WarnEmbed.add_field(name = "Unwarned user: ", value = f"{member.mention}")
        WarnEmbed.add_field(name = "Moderator: ", value = f"{ctx.message.author.mention}")
        WarnEmbed.add_field(name = "Warns: ", value = f"{warns[0]-1}")
        
        await ctx.message.delete()
        await ctx.send(embed = WarnEmbed)

def setup(bot):
    bot.add_cog(Admin(bot))
    print("Admin commands extension successfully registered")