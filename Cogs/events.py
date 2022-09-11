import discord
import datetime
from enums import Enums
from client import Aspid
from discord.ext import commands


class AspidEvents(commands.Cog):
    def __init__(self, bot: Aspid):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.lower() == 'f':
            m = await message.channel.send('🇫')
            reaction = self.bot.get_emoji(Enums.F)
            await m.add_reaction(reaction)
            try:
                await message.delete()
            except Exception:
                print('The message is already deleted!')
            return
        for i in ('aspid', 'аспид'):
            if i in message.content.lower():
                reaction = self.bot.get_emoji(Enums.Aspid)
                await message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.system_channel:
            lang = self.bot.get_languages(member.guild)
            embed = discord.Embed(
                title=lang['arrive_head'],
                description=f"**{member.name}" + lang['arrive'],
                color=discord.Colour.dark_green(),
            )
            embed.add_field(name= "** **", value=f"<t:{int(datetime.datetime.now().timestamp())}:R>") 
            embed.set_thumbnail(url= member.display_avatar.url)
            try:
                await member.guild.system_channel.send(embed=embed)
            except discord.errors.Forbidden:
                print(f'I cannot announce arrival on {member.guild.name}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.system_channel:
            lang = self.bot.get_languages(member.guild)
            embed = discord.Embed(
                title=lang['gone_head'],
                description=f"**{member.name}" + lang['gone'],
                color=discord.Colour.red(),
            )
            embed.add_field(name= "** **", value= f"<t:{int(datetime.datetime.now().timestamp())}:R>") 
            embed.set_thumbnail(url= member.display_avatar.url)
            try:
                await member.guild.system_channel.send(embed= embed)
            except discord.errors.Forbidden:
                    print(f'I cannot announce arrival on {member.guild.name}')

async def setup(bot):
    await bot.add_cog(AspidEvents(bot))
