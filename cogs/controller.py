import discord
import asyncio
from discord.ext import commands
from custom.database import Database
from custom.gpt import ClickbaitRating
from custom.scrape import Scraper

class Controller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database() 
        self.clickbait = ClickbaitRating()
        self.scraper = Scraper()

    @discord.app_commands.command(name="ttsetchannel")
    async def set_channel(self, interaction):
        self.db.set_channel(interaction.guild.id, interaction.channel_id)
        await interaction.response.send_message(f"channel set to {interaction.channel}")

async def setup(bot):
    await bot.add_cog(Controller(bot))
