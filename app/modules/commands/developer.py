import discord
from discord import app_commands
from discord.ext import commands

from app.bot import Carbon


class DeveloperCog(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    @app_commands.command(name="sync", description="Sync the command tree")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(
        self, interaction: discord.Interaction, guild_id: str | None = None
    ) -> None:
        """Syncs the command tree. If guild_id is provided, syncs to that guild."""
        if (
            interaction.user.id not in [self.bot.owner_id]
            and not interaction.user.guild_permissions.administrator
        ):
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
            await interaction.followup.send(
                f"Synced command tree to guild {guild_id}.", ephemeral=True
            )
        else:
            await self.bot.tree.sync()
            await interaction.followup.send(
                "Synced command tree globally.", ephemeral=True
            )


async def setup(bot: Carbon):
    await bot.add_cog(DeveloperCog(bot))
