import os
import yaml
import discord
from enums import Bcolors, Enums
from discord.ext import commands


class EmptyConfig(Exception):
    def __init__(self, config_path: str):
        self.message = f"Please, set up variables in {config_path}"
        super().__init__(Bcolors.FAIL + self.message + Bcolors.ENDC)


class Aspid(commands.Bot):
    def __init__(self, intents, activity, localization_folder, data_folder, config):
        self.data_folder = data_folder
        os.makedirs(self.data_folder, exist_ok=True)
        self.config_path = self.data_folder + config
        with open(self.config_path, "a+", encoding="utf8") as file:
            file.seek(0)
            self.config = yaml.safe_load(file)
            if type(self.config) is not dict:
                yaml.dump({"BOT_PREFIX": None, "DEAD": 0, "DISCORD_TOKEN": None}, file)
                raise EmptyConfig(self.config_path)
            elif self.config["BOT_PREFIX"] == "":
                raise EmptyConfig(self.config_path)
        super().__init__(
            command_prefix=self.config["BOT_PREFIX"],
            intents=intents,
            activity=activity,
            help_command=None,
        )
        self.__languages = {}
        self.languages = localization_folder
        self.custom_guilds_list = None
        self.characters = None
        self.grubs = None
        self.fumos = None

    @property
    def languages(self):
        return self.__languages

    @languages.setter
    def languages(self, folder: str):
        for f in os.listdir(folder):
            if f.endswith(".yml"):
                path = folder + "/" + f
                with open(path, encoding="utf8") as file:
                    self.__languages[f[:-4]] = yaml.safe_load(file)

    def get_languages(self, guild):
        return self.__languages[self.custom_guilds_list.at[guild.id, "language"]]

    async def create_new_role(self, guild):
        try:
            role = await guild.create_role(
                name=Enums.Dead, colour=discord.Colour.from_rgb(0, 0, 1)
            )
            return role
        except:
            print(f"Cannot create role on {guild.name}")
            return None

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=567767402062807055))

    async def on_command_error(self, ctx, error):
        print(error)
