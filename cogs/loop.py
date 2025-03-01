import discord
from discord.ext import commands
from custom.database import Database
from custom.scraper import Scraper
from custom.gpt import Clickbait
from datetime import datetime
import pytz

class Loop(commands.Cog):
    def __init__(self, bot):
        self.scraper = Scraper()
        self.bot = bot
        self.clickbait = Clickbait()
        self.recentheadline = None
        self.recentlink = None

    async def start_loop(self):
        pass

    @discord.app_commands.command(name="postnews")
    async def post_recent(self, interaction):
        if recentheadline:
            await interaction.response.send_message(f"# {self.recentheadline}\n{self.recentlink}")
        else:
            await interaction.response.send_message("No recent news")

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
    bot.add_cog(Loop(bot))