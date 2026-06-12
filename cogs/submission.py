import logging
import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy.orm import Session

from database import get_db
from models import Activity

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

    @app_commands.command(name="get_sample", description="get_sample")
    async def get_sample(
        self,
        interaction: discord.Interaction,
    ):
        
        db: Session = next(get_db())

        iiiii = db.query(Activity).all()
        print(iiiii)
        
        await interaction.response.send_message(f"pong {interaction.user.mention}!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SubmissionCog(bot))