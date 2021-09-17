import discord
from discord.ext import commands
import music
import os

cogs = [music]

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

token = os.environ.get('TOKEN')
if token == None:
    print("Go to https://discord.com/developers/applications select your bot and get your token")
    print("Use export command to set the TOKEN enviroment variable")
    print("Example: export TOKEN=MY-DISCORD-BOT-TOKEN")
    exit()
client.run(os.environ.get('TOKEN'))
