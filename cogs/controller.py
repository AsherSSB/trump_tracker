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

    @discord.app_commands.command(name="testnews")
    async def post_news(self, interaction):
        await interaction.response.send_message("Loading...")
        article = await self.get_most_controversial()
        await interaction.followup.send(f"# {article[0]}\n{article[1]}")

    async def get_most_controversial(self):
        articles = self.scraper.get_headlines()
        max_rating = -1
        best_index = None
        ratings = [0] * len(articles)

        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(self.generate_rating(article[0]), name=str(i))
                for i, article in enumerate(articles)
            ]

        for task in tasks:
            index = int(task.get_name())
            rating = task.result()  # Safe to access results now
            if rating > max_rating:
                max_rating = rating
                best_index = index

        return articles[best_index]

    async def generate_rating(self, headline):
        rating = await asyncio.to_thread(self.clickbait.generate_rating, headline)
        print(headline, rating)
        return float(rating)

async def setup(bot):
    await bot.add_cog(Controller(bot))
