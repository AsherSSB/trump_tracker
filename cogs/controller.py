import discord
from discord.ext import commands
from custom.database import Database

class Controller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database() 

    @discord.app_commands.command(name="enterserver")
    async def hello_world(self, interaction):
        self.db.enter_server(interaction.guild.id, interaction.channel_id)
        await interaction.response.send_message("Entered Server ID")

    @discord.app_commands.command(name="fetchchannel")
    async def fetch_channel(self, interaction):
        res = self.db.fetch_channel(interaction.guild.id)
        await interaction.response.send_message(res)


async def setup(bot):
    await bot.add_cog(Controller(bot))
