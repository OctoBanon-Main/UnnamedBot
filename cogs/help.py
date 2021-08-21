import discord, asyncio, datetime
from discord.ext import commands
from discord_components import DiscordComponents, InteractionType, ButtonStyle, Button

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        dc = DiscordComponents(bot)
    
    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        embedOne = discord.Embed(
            title = "User commands",
            description = "#",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        embedOne.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")

        embedTwo = discord.Embed(
            title = "Admin commands",
            description = "**u!ban** - Ban member **( Usage: u!ban @user Reason (Optional) )** \n **u!unban** - Unban member **( Usage: u!unban @user )** \n **u!kick** - Kick member **( Usage: u!kick @user Reason (Optional) )** \n **u!mute** - Mute member **( Usage: u!mute @user Reason (Optional) )** \n **u!unmute** - Unmute member **( Usage: u!unmute @user )** \n **u!clear** - Clear chat **( Usage: u!clear <ammout> )** \n **u!warn** - Give warning to server member **( Usage: u!warn @user Reason (Optional) )** \n **u!unwarn - Remove warning from server member **( Usage: u!unwarn @user )**",
            timestamp = datetime.datetime.utcnow(),
            colour = 0xcc9a68
        )
        embedTwo.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar_url}")

        paginationList = [embedOne, embedTwo]
        current = 0
        
        mainMessage = await ctx.send(
            embed = paginationList[current],
            components = [
                [
                    Button(
                        label = "Prev",
                        id = "back",
                        style = ButtonStyle.red
                    ),
                    Button(
                        label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                        id = "cur",
                        style = ButtonStyle.grey,
                        disabled = True
                    ),
                    Button(
                        label = "Next",
                        id = "front",
                        style = ButtonStyle.red
                    )
                ]
            ]
        )

        while True:
            try:
                interaction = await self.bot.wait_for(
                    "button_click",
                    check = lambda i: i.component.id in ["back", "front"], #You can add more
                    timeout = 10.0 #10 seconds of inactivity
                )
                if interaction.component.id == "back":
                    current -= 1
                elif interaction.component.id == "front":
                    current += 1
                if current == len(paginationList):
                    current = 0
                elif current < 0:
                    current = len(paginationList) - 1

                await interaction.respond(
                    type = InteractionType.UpdateMessage,
                    embed = paginationList[current],
                    components = [ #Use any button style you wish to :)
                        [
                            Button(
                                label = "Prev",
                                id = "back",
                                style = ButtonStyle.red
                            ),
                            Button(
                                label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                                id = "cur",
                                style = ButtonStyle.grey,
                                disabled = True
                            ),
                            Button(
                                label = "Next",
                                id = "front",
                                style = ButtonStyle.red
                            )
                        ]
                    ]
                )
           
            except asyncio.TimeoutError:
                await mainMessage.edit(
                    components = [
                        [
                            Button(
                                label = "Prev",
                                id = "back",
                                style = ButtonStyle.red,
                                disabled = True
                            ),
                            Button(
                                label = f"Timed out",
                                id = "cur",
                                style = ButtonStyle.grey,
                                disabled = True
                            ),
                            Button(
                                label = "Next",
                                id = "front",
                                style = ButtonStyle.red,
                                disabled = True
                            )
                        ]
                    ]
                )
                break

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
    print("Help command extension successfully registered")