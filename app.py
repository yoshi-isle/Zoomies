import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Import what you need
from database import init_db, SessionLocal, get_db
from models import Activity, Submission   # ← Full IntelliSense here

load_dotenv()


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )
        
        init_db()
        
        self.SessionLocal = SessionLocal
        self.Activity = Activity
        self.Submission = Submission

    async def setup_hook(self) -> None:
        cogs = ["cogs.submission", "cogs.static_embeds"]
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"{cog} loaded successfully.")
            except Exception as e:
                print(f"Failed to load {cog}: {e}")

    async def on_ready(self):
        await self.tree.sync()
        print(f"{self.user} has connected to Discord!")


bot = Bot()

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))