import json, discord
from discord.ext import commands

with open("config.json", "r") as read_file:
    config = json.load(read_file)

bot = commands.Bot(command_prefix=config["prefix"])

@bot.event
async def on_ready():
    init.startup()
    await bot.change_presence(activity=discord.Game(name=config["current_game"]))
    print("──────────────────────────────────────────")
    print("Bot is ready")
    print("Registered extensions: " + json.dumps(config["extensions"]))

# Loading extensions
if __name__ == '__main__':
    for extensions in config["extensions"]:
        bot.load_extension(extensions)

bot.run(config["token"])
