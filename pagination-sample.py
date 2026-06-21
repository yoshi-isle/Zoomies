import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button


class TestPager(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.current_page = 1
        self.max_pages = 8

    async def update_embed(self, interaction: discord.Interaction, new_image=""):
        embed = discord.Embed(
            title=f"Test {self.current_page}",
            description=f"This is page **{self.current_page}** of {self.max_pages}.",
            color=discord.Color.blue(),
        )
        embed.set_footer(text=f"4465465456456456")

        embed.set_image(url=new_image)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="World 1", style=discord.ButtonStyle.primary, custom_id="page_1"
    )
    async def page1(self, interaction: discord.Interaction, button: Button):
        self.current_page = 1
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/QBROp7f.png"
        )

    @discord.ui.button(
        label="World 2", style=discord.ButtonStyle.primary, custom_id="page_2"
    )
    async def page2(self, interaction: discord.Interaction, button: Button):
        self.current_page = 2
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/QBROp7f.png"
        )

    @discord.ui.button(
        label="World 3", style=discord.ButtonStyle.primary, custom_id="page_3"
    )
    async def page3(self, interaction: discord.Interaction, button: Button):
        self.current_page = 3
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/QBROp7f.png"
        )

    @discord.ui.button(
        label="World 4", style=discord.ButtonStyle.primary, custom_id="page_4"
    )
    async def page4(self, interaction: discord.Interaction, button: Button):
        self.current_page = 4
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/kYCOpML.png"
        )

    @discord.ui.button(
        label="World 5", style=discord.ButtonStyle.primary, custom_id="page_5"
    )
    async def page5(self, interaction: discord.Interaction, button: Button):
        self.current_page = 5
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/QBROp7f.png"
        )

    @discord.ui.button(
        label="World 6", style=discord.ButtonStyle.primary, custom_id="page_6"
    )
    async def page6(self, interaction: discord.Interaction, button: Button):
        self.current_page = 6
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/QBROp7f.png"
        )

    @discord.ui.button(
        label="World 7", style=discord.ButtonStyle.primary, custom_id="page_7"
    )
    async def page7(self, interaction: discord.Interaction, button: Button):
        self.current_page = 7
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/QBROp7f.png"
        )

    @discord.ui.button(
        label="World 8", style=discord.ButtonStyle.primary, custom_id="page_8"
    )
    async def page8(self, interaction: discord.Interaction, button: Button):
        self.current_page = 8
        await self.update_embed(
            interaction, new_image="https://i.imgur.com/QBROp7f.png"
        )


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="testpages")
    async def test_pages(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Test 1",
            description="This is page **1** of 8.",
            color=discord.Color.blue(),
        )
        embed.set_image(url="https://i.imgur.com/QBROp7f.png")
        embed.set_footer(text=f"test")

        view = TestPager()
        await interaction.channel.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(TestCog(bot))
