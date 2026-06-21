import logging
import discord
from discord.ext import commands
from discord import app_commands
from embeds import Embeds

class StaticEmbedCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Static embed cog initialized")

    @app_commands.command(name="the_hunt_winners", description="Displays the hunt winners")
    async def the_hunt_winners(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.channel.send(embed=Embeds.the_hunt_winners())
        await interaction.response.send_message(f"Displayed the hunt winners, {interaction.user.mention}!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(StaticEmbedCog(bot))