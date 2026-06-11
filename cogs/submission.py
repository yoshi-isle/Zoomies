import logging
import os
import discord
import asyncio
from typing import List
from discord.ext import commands, tasks
from discord import app_commands
from urllib.parse import urlparse


class SubmissionCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Submission cog initialized")

    @app_commands.command(name="ping", description="ping")
    async def ping(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(f"pong {interaction.user.mention}!", ephemeral=True)
        


async def setup(bot: commands.Bot):
    await bot.add_cog(SubmissionCog(bot))