import discord
from discord.ext import commands, tasks
import asyncio
from custom.database import Database
from custom.scrape import Scraper
from custom.gpt import ClickbaitRating
from datetime import datetime
import pytz

class Loop(commands.Cog):
    def __init__(self, bot):
        self.scraper = Scraper()
        self.bot = bot
        self.clickbait = ClickbaitRating()
        self.recentheadline = None
        self.recentlink = None
        self.db = Database()
        self.news_loop.start() 

    def cog_unload(self):
        self.news_loop.cancel()

    @tasks.loop(minutes=1)
    async def news_loop(self):
        now = datetime.now(pytz.timezone("US/Eastern"))
        target_times = [(11, 0), (22, 6)]  # 11:00 AM and 8:00 PM

        current_time = (now.hour, now.minute)
        if current_time in target_times:
            article = await self.get_most_controversial()
            self.recentheadline = article[0]
            self.recentlink = article[1]
            
            servers = self.db.get_all_servers()
            for guild_id, channel_id in servers:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send(f"# {self.recentheadline}\n{self.recentlink}")
                    except discord.errors.Forbidden:
                        print(f"Cannot send to channel {channel_id} in guild {guild_id}")

    @news_loop.before_loop
    async def before_news_loop(self):
        await self.bot.wait_until_ready()

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
            rating = task.result()
            if rating > max_rating:
                max_rating = rating
                best_index = index

        return articles[best_index]

    async def generate_rating(self, headline):
        rating = await asyncio.to_thread(self.clickbait.generate_rating, headline)
        print(headline, rating)
        return float(rating)


async def setup(bot):
    await bot.add_cog(Loop(bot))