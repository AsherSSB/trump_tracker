import discord
from discord.ext import commands
from custom.database import Database
from custom.gpt import ClickbaitRating

class Controller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database() 
        self.clickbait = ClickbaitRating()

    @discord.app_commands.command(name="ttsetserver")
    async def set_server(self, interaction):
        self.db.enter_server(interaction.guild.id, interaction.channel_id)
        await interaction.response.send_message("Server set")

    @discord.app_commands.command(name="ttfetchchannel")
    async def fetch_channel(self, interaction):
        res = self.db.fetch_channel(interaction.guild.id)
        await interaction.response.send_message(f"channel set to {interaction.channel}")
 
    @discord.app_commands.command(name="ttsetchannel")
    async def set_channel(self, interaction):
        self.db.set_channel(interaction.guild.id, interaction.channel_id)
        await interaction.response.send_message(f"channel set to {interaction.channel}")

    @discord.app_commands.command(name="testgpt")
    async def test_gpt(self, interaction, prompt: str):
        await interaction.response.send_message("logging...")
        res = self.clickbait.generate_rating(prompt)
        await interaction.followup.send(content=res)

async def setup(bot):
    await bot.add_cog(Controller(bot))
