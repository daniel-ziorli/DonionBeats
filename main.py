import discord
from discord.ext import commands
import music
import os
import json

cogs = [music]

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

f = None
try:
    f = open('config.json',)
except:
    print("Run 'make' command to set up your config")
    exit()

data = None
try:
    data = json.load(f)
except:
    print("Run 'make' command to set up your config")
    exit()

token = None
try:
    token = data["TOKEN"]
except:
    print("Run 'make' command to set up your config")
    exit()

if token == "" or token == None:
    print("Run 'make' command to set up your config")
    exit()

print(token)
client.run(str(token))
