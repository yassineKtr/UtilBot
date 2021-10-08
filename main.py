import discord
from discord.ext import commands
from discord.flags import Intents
import os
from dotenv import load_dotenv




load_dotenv()


DISCORD_TOKEN = os.getenv("TOKEN")

client = commands.Bot(command_prefix='?', Intents=discord.Intents.all())



@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') 



client.run(DISCORD_TOKEN)
