import random
import discord
import asyncio
import datetime
from enums import Enums
from client import Aspid
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot: Aspid):
        self.bot = bot

    @commands.command(name="pet", help="Pet an Aspid! Or others...")
    async def pet(self, ctx, *, target=""):
        await ctx.message.add_reaction(self.bot.get_emoji(Enums.Aspid))
        lang = self.bot.get_languages(ctx.guild)
        if target != "":
            victim = ctx.guild.get_member(int(target[2:-1]))
            if victim == ctx.author:
                await ctx.send(lang["pet_self"])
                return
            if victim.bot:
                await ctx.send(lang["pet_aspid"])
                return
            embed = discord.Embed(
                description=f"{victim.mention} {lang['is_pet']} {ctx.message.author.mention}",
                color=discord.Colour.magenta(),
            )
            await ctx.send(embed=embed)
            return
        role_dead = ctx.guild.get_role(
            self.bot.custom_guilds_list.at[ctx.guild.id, "dead"]
        )
        if role_dead is None:
            role_dead = await self.bot.create_new_role(ctx.guild)
            self.bot.custom_guilds_list.at[ctx.guild.id, "dead"] = (
                role_dead.id if role_dead is not None else 0
            )
        if role_dead in ctx.message.author.roles:
            await ctx.send(lang["pet_dead"])
            return
        a = lang["pet_opinions"]
        b = lang["pet_answers"]
        n1 = random.randint(0, len(a) - 1)
        n2 = random.randint(0, len(b) - 1)
        if n2 == 0:
            if role_dead is not None:
                try:
                    await ctx.message.author.add_roles(role_dead)
                except discord.errors.Forbidden:
                    print("Cannot add roles")
        await ctx.send(a[n1] + "\n" + b[n2])

    @commands.command(name="ask", help="Ask Aspid about something!")
    async def ask(self, ctx, *, message=""):
        await ctx.message.add_reaction(self.bot.get_emoji(Enums.Aspid))
        lang = self.bot.get_languages(ctx.guild)
        if message == "":
            await ctx.send(lang["ask_no"])
        else:
            await ctx.send(random.choice(lang["ask_answers"]))

    @commands.command(name="poll", help="Start a poll with stated question")
    async def poll(self, ctx, *, message=""):
        lang = self.bot.get_languages(ctx.guild)
        if len(message) < 1800:
            if message == "":
                await ctx.send(lang["vote_short"])
                return
            embed = discord.Embed(
                title=lang["vote_head"],
                description=f"**{message}**\n\n <:THK_Good:575051447599628311> {lang['vote_good']} \n <:THK_Bad:575796719078473738> {lang['vote_bad']}",
                color=discord.Colour.red(),
            )
            mes = await ctx.send(embed=embed)
            await mes.add_reaction(self.bot.get_emoji(Enums.Good))
            await mes.add_reaction(self.bot.get_emoji(Enums.Bad))

    @commands.command(name="join", help="Add Aspid to your server!", pass_context=True)
    async def join(self, ctx):
        lang = self.bot.get_languages(ctx.guild)
        await ctx.send("An invitation link has been sent to your pm!")
        embed = discord.Embed(
            title=lang["join"],
            color=discord.Colour.dark_green(),
            description=r"https://discordapp.com/oauth2/authorize?&client_id=581221797295554571&scope=bot&permissions=8",
        )
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/603600328117583874/615150515210420249/primal_aspid_king.gif"
        )
        try:
            await ctx.message.author.send(embed=embed)
        except:
            await ctx.send(lang["dm_fail"])

    @commands.command(name="code", help="github link")
    async def code(self, ctx):
        lang = self.bot.get_languages(ctx.guild)
        embed = discord.Embed(
            title=lang["code_head"],
            color=discord.Colour.red(),
            description=lang["code_body"],
        )
        embed.add_field(
            name="** **", value=f"<t:{int(datetime.datetime.now().timestamp())}:R>"
        )
        embed.set_image(
            url="https://media.discordapp.net/attachments/614108079545647105/629782304738377738/3032408cf9e547dc.png"
        )
        await ctx.send(embed=embed)

    @commands.command(name="grub", help="Take a look at these grubs!")
    async def grub(self, ctx):
        await ctx.message.add_reaction(self.bot.get_emoji(Enums.Grub))
        embed = discord.Embed(color=discord.Colour.dark_green())
        embed.set_image(url=random.choice(self.bot.grubs))
        await ctx.send(embed=embed)

    @commands.command(aliases=["daddy"], help="On your own risk")
    async def batya(self, ctx):
        embed = discord.Embed(color=discord.Colour.dark_green())
        embed.set_image(
            url="https://media.discordapp.net/attachments/614108079545647105/1015285820669833358/unknown.png"
        )
        await ctx.send(embed=embed)

    @commands.command(name="pick", help="let aspid help you make a choice")
    async def pick(self, ctx, *, text=""):
        if text == "":
            await ctx.send("pick a | b | c")
        else:
            g = text.split("|")
            g = [i.strip() for i in g]
            try:
                await ctx.send(random.choice(g))
            except discord.errors.HTTPException:
                print("Wrong input")

    @commands.command(
        name="message", help="Post a message as a server itself", pass_context=True
    )
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, arg):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name="Aspid")
        await webhook.send(
            content=arg, username=ctx.guild.name, avatar_url=ctx.guild.icon.url
        )
        await webhook.delete()

    @commands.command(name="server", help="get server info", pass_context=True)
    async def server(self, ctx):
        lang = self.bot.get_languages(ctx.guild)
        await ctx.message.delete()
        text = (
            lang["server_1"]
            + ctx.guild.name
            + lang["server_2"]
            + f"<t:{int(ctx.guild.created_at.timestamp())}:R>\n\n"
            + lang["server_3"]
            + str(len(ctx.guild.members))
            + lang["server_4"]
            + str(len(ctx.guild.roles))
            + lang["server_5"]
            + str(len(ctx.guild.channels))
            + lang["server_6"]
        )
        embed = discord.Embed(
            color=discord.Colour.purple(), timestamp=datetime.datetime.today()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name=lang["server_head"], value=text)
        await ctx.send(embed=embed)

    @commands.command(name="techo", help="Temporary message for up to 600 sceonds")
    async def techo(self, ctx, _time=" ", *, arg=""):
        try:
            _time = int(_time)
        except ValueError:
            await ctx.send(
                f"Command must be in format `{self.bot.config['BOT_PREFIX']}techo <0-600> text`"
            )
            return
        if _time > 600 or _time < 0:
            await ctx.send("Time can be set anly between 0 and 600 seconds")
            return
        try:
            await ctx.message.delete()
        except:
            pass
        mes = await ctx.send(arg)
        await asyncio.sleep(_time)
        await mes.delete()

    @commands.command(name="blend", help="Blend all symbols in sentence")
    async def techo(self, ctx, *, arg):
        output = list(arg)
        random.shuffle(output)
        await ctx.send("".join(output))

    @commands.command(name="fumo")
    async def fumo(self, ctx):
        await ctx.message.add_reaction(self.bot.get_emoji(Enums.Fumo))
        await ctx.send(random.choice(self.bot.fumos))


async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
