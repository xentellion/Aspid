import discord
from enums import Enums
from client import Aspid
from discord import app_commands
from discord.ext import commands


class PageButton(discord.ui.View):
    def __init__(self, lang: dict) -> None:
        super().__init__(timeout=None)
        self.titles = lang["help_titles"]
        self.texts = lang["help"]
        self.add_buttons()

    async def page_1(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=discord.Colour.red(), description=self.texts[0])
        embed.set_thumbnail(url=Enums.aspid_1)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def page_2(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=discord.Colour.dark_green(), description=self.texts[1]
        )
        embed.set_thumbnail(url=Enums.aspid_2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def page_3(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=discord.Colour.blurple(), description=self.texts[2]
        )
        embed.set_thumbnail(url=Enums.aspid_3)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    def add_buttons(self):
        methods = [self.page_1, self.page_2, self.page_3]
        for i in range(len(self.titles)):
            button = discord.ui.Button(
                label=self.titles[i], style=discord.ButtonStyle.gray
            )
            button.callback = methods[i]
            self.add_item(button)


class Slash(commands.Cog):
    def __init__(self, bot: Aspid):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="help", description="List of Aspid commands")
    async def slash_help(self, interaction: discord.Interaction):
        lang = self.bot.get_languages(interaction.guild)
        view = PageButton(lang)
        embed = discord.Embed(
            colour=discord.Colour.yellow(),
            title=lang["help_header"],
            description=lang["help_description"],
        )
        embed.set_thumbnail(url=interaction.client.user.avatar)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: Aspid):
    await bot.add_cog(Slash(bot))
