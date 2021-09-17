import discord
from discord.ext import commands
import music

cogs = [music]

client = commands.Bot(command_prefix="-", intents = discord.Intents.all())

for i in range(len(cogs)):
  cogs[i].setup(client);

token = None
if token == None:
  print('put your token in ')
client.run(token)
