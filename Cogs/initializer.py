import pytz
import yaml
import discord
import asyncio
import pandas as pd
from client import Aspid
from enums import Bcolors, Enums
from datetime import datetime, time
from discord.ext import commands, tasks


class Initialize(commands.Cog):
    def __init__(self, bot: Aspid):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Bcolors.FAIL}{self.bot.user.name} has connected to Discord{Bcolors.ENDC}')
        self.bot.grubs = await self.get_image_collections(Enums.GrubChannel)
        self.bot.fumos = await self.get_image_collections(Enums.FumoChannel, True)
        await self.get_guilds()
        await self.get_characters()
        tz = pytz.timezone("Europe/Moscow")
        now = datetime.now(tz)
        midnight = tz.localize(datetime.combine(now.date(), time(0, 0)), is_dst=None)
        delay = (midnight - now).seconds
        print(f"Aspid delay - {delay}")
        await asyncio.sleep(delay)
        await self.reminder.start()

    async def get_guilds(self):
        path = self.bot.data_folder + 'guilds.csv'
        f = open(path, 'a+', encoding='utf-8')
        f.close()
        try:
            df = pd.read_csv(path, index_col= 0)
        except pd.errors.EmptyDataError:
            columns = ['name', 'dead', 'language']
            df = pd.DataFrame(columns= columns) 
        for guild in self.bot.guilds:
            if guild.id not in df.index:  
                d_r = await self.get_role(guild)
                if d_r is None:
                    role = await self.bot.create_new_role(guild)
                    d_r = 0 if role is None else role.id
                else:
                    d_r = d_r.id
                df.loc[guild.id] = [guild.name, d_r, guild.preferred_locale]
            else:
                d_r = await self.get_role(guild, df.at[guild.id, 'dead'])
                if d_r is None:
                    role = await self.bot.create_new_role(guild)
                    df.at[guild.id, 'dead'] = role.id if role is not None else 0
        self.bot.custom_guilds_list = df
        df.to_csv(path)
        print(f'{Bcolors.BOLD}> Total servers: {len(df.index)}')

    async def get_characters(self):
        path = self.bot.data_folder + Enums.default_char_list
        f = open(path, 'a+', encoding='utf-8')
        f.close()
        try:
            df = pd.read_csv(path, index_col= 0)
        except pd.errors.EmptyDataError:
            columns = ['user', 'login', 'avatar']
            df = pd.DataFrame(columns= columns)
        self.bot.characters = df
        df.to_csv(path)
        print(f'> Total characters: {len(df.index)}{Bcolors.ENDC}')

    async def get_role(self, guild, role_id = -1):
        return discord.utils.get(
            guild.roles, 
            name= Enums.Dead
            ) if role_id == -1 else guild.get_role(role_id)

    async def get_image_collections(self, id, fumos = False):
        collection = await self.bot.fetch_channel(id)
        collection = [message async for message in collection.history(limit=200)]
        return [i.content if fumos else i.attachments[0].url for i in collection]
  
    @tasks.loop(hours= 12)
    async def reminder(self):
        # ch = await self.bot.fetch_channel(Enums.AspidChannel)
        # embed = discord.Embed(color = discord.Colour.red())
        # embed.set_image(url= "https://media.discordapp.net/attachments/614108079545647105/614108112730718249/primal_aspid.jpg?width=676&height=474")
        # await ch.send(embed=embed)
        count = 0
        for guild in self.bot.guilds:
            role = guild.get_role(self.bot.custom_guilds_list.at[guild.id, 'dead'])
            if guild.me.guild_permissions.manage_roles:
                for user in guild.members:
                    if role in user.roles:
                        try:
                            await user.remove_roles(role)
                            count += 1
                        except:
                            continue
        dead = int(self.bot.config['DEAD'])
        dead += count
        self.bot.config['DEAD'] = dead
        with open(self.bot.config_path, 'w', encoding="utf8") as file:
            yaml.dump(self.bot.config, file)

    @commands.command(name='sync') 
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx) -> None:
        synced = await ctx.bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands globally")
        return

async def setup(bot):
    await bot.add_cog(Initialize(bot))
