import logging
import os
import redis.asyncio as redis
import discord
import asyncio
from typing import List
from discord.ext import commands, tasks
from discord import app_commands
from flask import json
from constants.emojis import EMOJIS
from redis import Redis
from urllib.parse import urlparse
from constants.submittable_tasks import TASKS
from constants.channel_ids import SUBMISSIONS_CHANNEL_ID


class SubmissionCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger | None = None):
        self.bot = bot
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Submission cog initialized")

        redis_url = os.getenv("REDIS_CONNECTION_STRING", "redis://localhost:6379")
        parsed_url = urlparse(redis_url)
        self.redis_host = parsed_url.hostname
        self.redis_port = parsed_url.port
        self.redis_submissions = redis.Redis(
            host=self.redis_host, port=self.redis_port, db=0
        )
        self.redis_processed = redis.Redis(
            host=parsed_url.hostname,
            port=parsed_url.port,
            db=1,
        )
        self.redis_listener.start()

    def cog_unload(self):
        self.redis_listener.cancel()

    async def record_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=item, value=item)
            for item in TASKS
            if current.lower() in item.lower()
        ]

    @app_commands.command(name="submit", description="Submit a PB")
    @app_commands.describe(
        item="Select the record category you're submitting for",
        members="Enter the Discord @mentions of all team members involved, separated by commas",
        image="Upload an image/screenshot of your personal best",
    )
    @app_commands.autocomplete(item=record_autocomplete)
    async def submit(
        self,
        interaction: discord.Interaction,
        item: str,
        members: str,
        image: discord.Attachment,
    ):
        await self.redis_submissions.lpush(
            "submissions",
            json.dumps(
                {
                    "record": item,
                    "image_url": image.url if image else None,
                    "user_id": str(interaction.user.id),
                    "members": members,
                }
            ),
        )
        await interaction.response.send_message(
            f"Your PB request has been submitted: {item}!\nYou'll be notified when processing is complete.",
            ephemeral=True,
        )

    @tasks.loop()
    async def redis_listener(self):
        """Listen for processed images from Redis"""
        try:
            result = await self.redis_processed.brpop("pb_ready", timeout=1)
            if result:
                _, message = result
                data = json.loads(message)
                await self.handle_new_submission(data)

        except Exception as e:
            self.logger.error(f"Redis listener error: {e}")
            await asyncio.sleep(1)

    async def handle_new_submission(self, data):
        try:
            imgur_url = data.get("imgur_url")
            members = data.get("members")
            record = data.get("record", "Unknown task")

            if imgur_url and members:
                channel = self.bot.get_channel(SUBMISSIONS_CHANNEL_ID)

                embed = discord.Embed(
                    title="New Submission",
                    description=f"**Activity:** {record}\n**Members:** {members}\n**Time:** 0:00",
                    color=discord.Color.yellow(),
                )
                embed.set_image(url=imgur_url)
                msg = await channel.send(embed=embed)
                await msg.add_reaction(EMOJIS.APPROVE)
                await msg.add_reaction(EMOJIS.DENY)

        except Exception as e:
            self.logger.error(f"Error handling processed image: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(SubmissionCog(bot))