import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import logging
import asyncio


class Bot(commands.Bot):
    def __init__(self):
        load_dotenv()
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        await self.tree.sync()
        print(f"{self.user} has connected to Discord!")


bot = Bot()

if __name__ == "__main__":

    async def main():
        discord.utils.setup_logging(level=logging.INFO)

        # Run the Discord bot
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))

    asyncio.run(main())
