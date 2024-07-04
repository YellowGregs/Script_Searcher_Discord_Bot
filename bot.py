import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from config.config import TOKEN
from cogs.search import SearchCog

load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_searches = {}

    async def setup_hook(self):
        await self.add_cog(SearchCog(self))
        await self.tree.sync()

bot = MyBot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    activity = discord.Game(name="Script Searcher | !search and /search")
    await bot.change_presence(activity=activity)
    print(f"Bot is ready 🤖 | Serving in {len(bot.guilds)} servers")

async def run_bot():
    while True:
        try:
            await bot.start(TOKEN)
        except (discord.ConnectionClosed, discord.GatewayNotFound) as e:
            print(f"Disconnected due to: {e}. Attempting to reconnect...")
            await asyncio.sleep(5)

if TOKEN is not None:
    asyncio.run(run_bot())
else:
    print("Error: Token is None. Please set a valid BOT_TOKEN in your environment.")
