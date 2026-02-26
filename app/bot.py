import discord
from discord.ext import commands


class Carbon(commands.Bot):
    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        intents.guilds = True
