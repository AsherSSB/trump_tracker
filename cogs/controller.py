import discord
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

    @discord.app_commands.command(name="testscrape")
    async def test_scrape(self, interaction):
        await interaction.response.send_message("logging...")
        res = self.scraper.get_headlines()
        print(res)

    @discord.app_commands.command(name="controversey")
    async def post_controversial(self, interaction):
        await interaction.response.send_message("logging")
        articles = self.scraper.get_headlines()
        max_rating = -1
        best_index = None
        for index, headline in enumerate([article[0] for article in articles]):
            rating = float(self.clickbait.generate_rating(headline))
            if rating > max_rating:
                max_rating = rating
                best_index = index
            print(headline, rating)
        print("\n\nBEST: " + articles[best_index][0])


async def setup(bot):
    await bot.add_cog(Controller(bot))
