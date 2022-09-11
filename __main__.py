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

path = os.path.realpath(__path__)

aspid = Aspid(
    intents = intents,
    activity = activity,
    data_folder= f'{path}/Data/',
    localization_folder= f'{path}/Localization/',
    config= 'config.yml'
)

async def main():
    for f in os.listdir(f'{path}/Cogs'):
        if f.endswith('.py'):
            await aspid.load_extension(f'Cogs.{f[:-3]}')
    await aspid.start(aspid.config['DISCORD_TOKEN'])

asyncio.run(main())
