import discord
from discord.ext import commands
from discord.flags import Intents
import os
from dotenv import load_dotenv
import Music

cogs = [Music]





load_dotenv()


DISCORD_TOKEN = os.getenv("TOKEN")

client = commands.Bot(command_prefix='?', Intents=discord.Intents.all())


for i in range(len(cogs)):
    cogs[i].setup(client)


client.run(DISCORD_TOKEN)
