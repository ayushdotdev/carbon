import discord


def not_bot(interaction: discord.Interaction) -> bool:
    return not interaction.user.bot
