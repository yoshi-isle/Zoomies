import logging
import os
import discord
from discord.ext import commands
import sys
from pathlib import Path
from embeds import Embeds
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
        await message.delete()

        # Find the PB leaderboard embed by category and update it
        pb_channel = self.bot.get_channel(int(os.getenv("PB_CHANNEL")))

        if not pb_channel:
            self.logger.critical(
                "[Approval Cog] PB channel does not exist. The service will not work properly. Exiting",
                ephemeral=True,
            )
            return

        # Get the category from the submission record
        submission = pb_service.get_pb_submission_by_id(int(footer))
        activity = pb_service.get_activity_by_id(submission.activity)
        category = activity.category

        print(category)

        pb_category_reprocess = pb_service.get_pb_category_reprocess_by_category(
            category
        )

        if not pb_category_reprocess:
            self.logger.critical(
                "[Approval Cog] No pb_category_reprocess record found for category. The service will not work properly. Exiting",
                ephemeral=True,
            )
            return

        leaderboard_message = await pb_channel.fetch_message(
            int(pb_category_reprocess.discord_message_id)
        )

        if not leaderboard_message:
            self.logger.critical(
                "[Approval Cog] No leaderboard message found for category. The service will not work properly. Exiting",
                ephemeral=True,
            )
            return

        embed = Embeds.pb_category(pb_service.get_top_pbs_for_category(category))
        await leaderboard_message.edit(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ApprovalCog(bot))
