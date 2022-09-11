import yaml
import random
import asyncio
import discord
from enums import Enums
from client import Aspid
from discord.ext import commands


class ShootingCommands(commands.Cog):
    def __init__(self, bot: Aspid):
        self.bot = bot

    @commands.command(name="shoot", help="ping user to try to kill them", pass_context=True)
    async def shoot(self, ctx, ping):
        await ctx.message.add_reaction(self.bot.get_emoji(Enums.Gun))
        lang = self.bot.get_languages(ctx.guild)
        victim = ctx.guild.get_member(int(ping[2:-1]))
        role_dead = ctx.guild.get_role(self.bot.custom_guilds_list.at[ctx.guild.id, 'dead'])
        if role_dead is None:
            role_dead = await self.bot.create_new_role(ctx.guild)
            self.bot.custom_guilds_list.at[ctx.guild.id, 'dead'] = role_dead.id if role_dead is not None else 0
        if role_dead in ctx.message.author.roles:
            await ctx.send(lang['shoot_dead'])
            return
        if ctx.author == victim:
            await ctx.send(lang['shoot_self'])
            return
        if victim == self.bot.user:
            await ctx.send(lang['shoot_aspid'])
            return
        if role_dead in victim.roles:
            await ctx.send(lang['shoot_at_dead'])
            return
        n = random.randint(0, 1)
        if n == 0:
            if role_dead is not None:
                try:
                    await victim.add_roles(role_dead)
                except discord.errors.Forbidden:
                    print('Cannot add roles')
            await ctx.send(lang['shoot.a'] + f'{ping}')
        else:
            await ctx.send(lang['shoot.b'])

    @commands.command(name="gun", help="russian roulette", pass_context=True)
    async def gun(self, ctx):
        async with ctx.typing():
            await ctx.message.add_reaction(self.bot.get_emoji(Enums.Gun))
            lang = self.bot.get_languages(ctx.guild)
            role_dead = ctx.guild.get_role(self.bot.custom_guilds_list.at[ctx.guild.id, 'dead'])
            if role_dead is None:
                role_dead = await self.bot.create_new_role(ctx.guild)
                self.bot.custom_guilds_list.at[ctx.guild.id, 'dead'] = role_dead.id if role_dead is not None else 0
            if role_dead in ctx.message.author.roles:
                await ctx.send(lang['gun_dead'])
                return
            await ctx.send(lang['gun_1'])    
            async with ctx.typing():
                await asyncio.sleep(2)
                await ctx.send(lang['gun_2'])
            async with ctx.typing():
                await asyncio.sleep(2)
                await ctx.send(lang['gun_3'])
            async with ctx.typing():
                await asyncio.sleep(4)
        n = random.randint(0, 6)
        if n == 0:
            if role_dead is not None:
                try:
                    await ctx.message.author.add_roles(role_dead)
                except discord.errors.Forbidden:
                    print('Cannot add roles')
            await ctx.send(f"{lang['gun_4.a.1']} {ctx.author.mention} {lang['gun_4.a.2']}")
        else:
            await ctx.send(lang['gun_4.b'])

    @commands.command(name="save", help="return the dead to life*", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def save(self, ctx):
        await ctx.message.add_reaction(self.bot.get_emoji(Enums.Gun))
        lang = self.bot.get_languages(ctx.guild)
        role_dead = ctx.guild.get_role(self.bot.custom_guilds_list.at[ctx.guild.id, 'dead'])
        if role_dead is None:
            role_dead = await self.bot.create_new_role(ctx.guild)
            self.bot.custom_guilds_list.at[ctx.guild.id, 'dead'] = role_dead.id if role_dead is not None else 0
        count = 0
        for i in ctx.guild.members:
            if role_dead in i.roles:
                await i.remove_roles(role_dead)
                count += 1
        dead = int(self.bot.config['DEAD'])
        dead += count
        self.bot.config['DEAD'] = dead
        with open(self.bot.config_path, 'w', encoding="utf8") as file:
            yaml.dump(self.bot.config, file)
        embed = discord.Embed(
            title= lang['save_0'],
            description= f"**{count}** {lang['save_1']} **{dead}** {lang['save_2']}"
        )
        embed.set_thumbnail(url= Enums.aspid_5)
        await ctx.send(embed= embed)

async def setup(bot):
    await bot.add_cog(ShootingCommands(bot))
