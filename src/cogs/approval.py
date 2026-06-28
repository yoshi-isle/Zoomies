import logging
import os
import discord
from discord.ext import commands
import sys
from pathlib import Path
from services import pb_service

# Get sibling dependencies
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


class ApprovalCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Approval cog initialized")

    # React to check or x emoji in a certain approval channel
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        print("on_raw_reaction_add")
        approval_channel = self.bot.get_channel(int(os.getenv("APPROVAL_CHANNEL")))

        if (
            payload.user_id == self.bot.user.id
            or payload.channel_id != approval_channel.id
        ):
            return

        guild = self.bot.get_guild(payload.guild_id)
        this_channel = guild.get_channel(payload.channel_id)
        message = await this_channel.fetch_message(payload.message_id)
        emoji = str(payload.emoji)
        changelog_channel = self.bot.get_channel(int(os.getenv("CHANGELOG_CHANNEL")))

        # --- Guard against Approval and Changelog channels ---
        if not approval_channel:
            self.logger.critical(
                "[Approval Cog] Approval channel does not exist. The service will not work properly. Exiting",
                ephemeral=True,
            )
            return

        if not changelog_channel:
            self.logger.critical(
                "[Approval Cog] Changelog channel does not exist. The service will not work properly. Exiting",
                ephemeral=True,
            )
            return

        # --- Handle approval or denial ---
        if emoji != "✅" and emoji != "❌":
            self.logger.info(
                f"[Approval Cog] Reaction {emoji} is not a check or X. Ignoring"
            )
            return

        embed = message.embeds[0]  # The embed footer contains the submission ID
        footer = embed.footer.text

        if not footer:
            self.logger.info(
                "[Approval Cog] No footer found in the embed. Cannot approve or deny the submission"
            )
            return

        self.logger.info(f"[Approval Cog] Approval received for message: {footer}")
        self.logger.info(
            f"[Approval Cog] Found ID {footer} in the message footer. Attempting to approve it by ID"
        )

        pb_service.approve_or_deny_pb_submission(int(footer), True)
        await changelog_channel.send("New pb submission has been approved")


async def setup(bot: commands.Bot):
    await bot.add_cog(ApprovalCog(bot))
