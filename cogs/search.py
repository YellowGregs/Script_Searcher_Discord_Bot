import discord
from discord.ext import commands
from discord import app_commands
import requests
import asyncio
import random
from utils.helpers import execute_search

class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, query=None, mode='free'):
        await execute_search(ctx, query, mode, prefix=True, bot=self.bot)

    @app_commands.command(name="search", description="Search for scripts")
    @app_commands.describe(query="The search query", mode="Search mode ('free' or 'paid')")
    async def slash_search(self, interaction: discord.Interaction, query: str = None, mode: str = 'free'):
        ctx = await self.bot.get_context(interaction)
        await execute_search(ctx, query, mode, prefix=False, bot=self.bot)