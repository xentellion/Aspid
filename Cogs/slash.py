import discord
import pandas as pd
from enums import Enums
from typing import List
from client import Aspid
from discord import app_commands
from discord.ext import commands


class PageButton(discord.ui.View):
    def __init__(self, lang: dict) -> None:
        super().__init__(timeout= None)
        self.titles = lang['help_titles']
        self.texts = lang['help']
        self.add_buttons()

    async def page_1(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour= discord.Colour.red(),
            description= self.texts[0]
        )
        embed.set_thumbnail(url= Enums.aspid_1)
        await interaction.response.send_message(embed= embed, ephemeral=True)

    async def page_2(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour= discord.Colour.dark_green(),
            description= self.texts[1]
        )
        embed.set_thumbnail(url= Enums.aspid_2)
        await interaction.response.send_message(embed= embed, ephemeral=True)

    async def page_3(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour= discord.Colour.blurple(),
            description= self.texts[2]
        )
        embed.set_thumbnail(url= Enums.aspid_3)
        await interaction.response.send_message(embed= embed, ephemeral=True)

    async def page_4(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour= discord.Colour.blue(),
            description= self.texts[3]
        )
        embed.set_thumbnail(url= Enums.aspid_4)
        await interaction.response.send_message(embed= embed, ephemeral=True)

    def add_buttons(self):     
        methods = [self.page_1, self.page_2, self.page_3, self.page_4]
        for i in range(len(self.titles)):
            button = discord.ui.Button(
                label= self.titles[i], 
                style= discord.ButtonStyle.gray
            )
            button.callback = methods[i]
            self.add_item(button)


class DeleteConfirm(discord.ui.View):
    def __init__(self, bot:Aspid, lang: dict, char) -> None:
        super().__init__(timeout= 10)
        self.bot = bot
        self.char = char
        self.titles = lang['char_delete_choice']
        self.lang = lang
        self.add_buttons()

    async def page_yes(self, interaction: discord.Interaction):
        self.bot.characters = self.bot.characters.drop(self.char.index[0])
        path = self.bot.data_folder + 'characters.csv'
        self.bot.characters.to_csv(path)
        self.bot.characters = pd.read_csv(path, index_col= 0)
        await interaction.response.send_message(self.lang["char_delete"], ephemeral=True)

    async def page_no(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.lang["char_delete_cancel"], ephemeral=True)
        await interaction.delete_original_response()
        self.clear_items()

    def add_buttons(self):     
        colors = [
            discord.ButtonStyle.red, 
            discord.ButtonStyle.green 
        ]
        methods = [
            self.page_yes, 
            self.page_no 
        ]
        for i in range(len(methods)):
            button = discord.ui.Button(label= self.titles[i], style= colors[i])
            button.callback = methods[i]
            self.add_item(button)


class Form(discord.ui.Modal):  
    login = discord.ui.TextInput(
        label= 'temp',
        style= discord.TextStyle.short,
        placeholder= "SampleLogin",
        required= True,
        min_length= 3,
        max_length=15
    )

    avatar = discord.ui.TextInput(
        label= 'temp',
        style=discord.TextStyle.short,
        required= False
    )

    def __init__(self, bot:Aspid, lang:dict):      
        self.bot = bot
        self.lang = lang
        super().__init__(title=self.lang["char_form"])
        self.login.label = self.lang["char_login"]
        self.avatar.label = self.lang["char_avatar"]
        self.avatar.placeholder = self.lang["char_avatar_link"]

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title = f'**{self.login}** {self.lang["char_join"]}')
        embed.set_author(name = interaction.user, icon_url=interaction.user.avatar.url)
        avatar = self.avatar if self.avatar.value != '' else Enums.default_image
        embed.set_thumbnail(url= avatar)
        self.bot.characters.loc[len(self.bot.characters.index)] = [interaction.user.id, self.login, avatar]
        path = self.bot.data_folder + Enums.default_char_list
        self.bot.characters.to_csv(path)
        self.bot.characters = pd.read_csv(path, index_col= 0)
        await interaction.response.send_message(embed= embed)


class Slash(commands.Cog):
    def __init__(self, bot: Aspid):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="help", description= "List of Aspid commands")
    @app_commands.guilds(discord.Object(id= 567767402062807055))
    async def slash_help(self, interaction: discord.Interaction):
        lang = self.bot.get_languages(interaction.guild)
        view = PageButton(lang)
        embed = discord.Embed(
            colour= discord.Colour.yellow(),
            title= lang["help_header"],
            description= lang["help_description"],
        )
        embed.set_thumbnail(url= interaction.client.user.avatar)
        await interaction.response.send_message(embed= embed, view= view, ephemeral= True)


    @app_commands.command(name="twitter", description= "Log in to write as your character")
    @app_commands.guilds(discord.Object(id= 567767402062807055))
    async def twitter_login(self, interaction: discord.Interaction):
        lang = self.bot.get_languages(interaction.guild)
        await interaction.response.send_modal(Form(self.bot, lang))

    async def rps_autocomplete(self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        choices = self.bot.characters.loc[self.bot.characters['user'] == interaction.user.id]['login']
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ]

    @app_commands.command(name="twit", description= "Write as your character!")
    @app_commands.autocomplete(choices=rps_autocomplete)
    @app_commands.guilds(discord.Object(id= 567767402062807055))
    async def twitter_post(self, interaction: discord.Interaction, choices:str, *, text:str):
        df = self.bot.characters
        char = df.loc[(df['user'] == interaction.user.id) & (df['login'] == choices)]
        webhook = await interaction.channel.create_webhook(name='Aspid')
        msg = await webhook.send(
            content= text, 
            username= f"{df.at[char.index[0], 'login']}", 
            avatar_url= f"{df.at[char.index[0], 'avatar']}",
            wait= True)
        await webhook.delete()
        await msg.add_reaction("💙")
        await interaction.response.send_message("✅", ephemeral=True)

    @app_commands.command(name="delete_twitter", description= "Delete your character")
    @app_commands.autocomplete(choices=rps_autocomplete)
    @app_commands.guilds(discord.Object(id= 567767402062807055))
    async def twitter_delete(self, interaction: discord.Interaction, choices:str):
        lang = self.bot.get_languages(interaction.guild)
        df = self.bot.characters
        char = df.loc[(df['user'] == interaction.user.id) & (df['login'] == choices)]
        await interaction.response.send_message(
            lang["char_delete_confirm"], 
            view= DeleteConfirm(self.bot, lang, char), 
            ephemeral= True
        )


async def setup(bot: Aspid):
    await bot.add_cog(Slash(bot))