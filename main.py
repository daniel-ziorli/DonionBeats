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
    print("set your token with 'export TOKEN=VALUE'")
    exit()
client.run(os.environ.get('TOKEN'))
