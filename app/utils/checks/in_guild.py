import discord


def in_guild(interaction: discord.Interaction) -> bool:
    return interaction.guild is not None
