import os
import asyncio
import discord
from client import Aspid


intents = discord.Intents.all()
intents.members = True
activity = discord.Activity(
    type=discord.ActivityType.listening, 
    name = "ваши крики | /help"
)

aspid = Aspid(
    intents = intents,
    activity = activity,
    data_folder= './Data/',
    localization_folder= './Localization/',
    config= 'config.yml'
)

async def main():
    for f in os.listdir('./Cogs'):
        if f.endswith('.py'):
            await aspid.load_extension(f'Cogs.{f[:-3]}')
    await aspid.start(aspid.config['DISCORD_TOKEN'])

asyncio.run(main())
