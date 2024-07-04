import requests
import discord
import asyncio
import random
from utils.formatters import create_embed
from utils.view_manager import display_scripts

async def execute_search(ctx, query, mode, prefix, bot):
    user_id = ctx.author.id
    try:
        if user_id in bot.active_searches:
            message = await ctx.send("You already have an active search running. Please wait for the first command to be complete.")
            await asyncio.sleep(random.randint(5, 10))
            await message.delete()
            return

        bot.active_searches[user_id] = True

        if query is None:
            help_message = (
                "Use `!search <query>` to find scripts.\n\n"
                "You can specify the search mode (default is `free`).\n"
                "**Modes**: `free`, `paid`\n"
                "**Example**: `!search arsenal paid`\n\n"
                "Please provide a query to get started."
            )
            initial_embed = discord.Embed(
                title="🔍 Script Search Help",
                description=help_message,
                color=0x3498db
            )
            initial_embed.set_thumbnail(url="https://media1.tenor.com/m/j9Jhn5M1Xw0AAAAd/neuro-sama-ai.gif")
            await ctx.send(embed=initial_embed)
            del bot.active_searches[user_id]
            return

        page = 1
        scriptblox_api_url = f"https://scriptblox.com/api/script/search?q={query}&mode={mode}&page={page}"

        scriptblox_response = requests.get(scriptblox_api_url)
        scriptblox_response.raise_for_status()
        scriptblox_data = scriptblox_response.json()

        if "result" in scriptblox_data and "scripts" in scriptblox_data["result"]:
            scripts = scriptblox_data["result"]["scripts"]

            if not scripts:
                error_embed = discord.Embed(
                    title="No Scripts Found",
                    description=f"No scripts found for: `{query}`",
                    color=0xff0000
                )
                error_embed.set_image(url="https://w0.peakpx.com/wallpaper/346/996/HD-wallpaper-love-live-sunshine-404-error-love-live-sunshine-anime-girl-anime.jpg")
                await ctx.send(embed=error_embed)
                del bot.active_searches[user_id]
                return

            message = await ctx.send("Fetching data...")

            await display_scripts(ctx, message, scripts, page, scriptblox_data["result"]["totalPages"], prefix, bot)
        else:
            error_embed = discord.Embed(
                title="No Scripts Found",
                description=f"No scripts found for: `{query}`",
                color=0xff0000
            )
            error_embed.set_image(url="https://w0.peakpx.com/wallpaper/346/996/HD-wallpaper-love-live-sunshine-404-error-love-live-sunshine-anime-girl-anime.jpg")
            await ctx.send(embed=error_embed)
    except requests.RequestException as e:
        await ctx.send(f"An error occurred: {e}")
    except KeyError as ke:
        await ctx.send(f"An error occurred while processing your request. Please try again later. Error: {ke}")
    finally:
        if user_id in bot.active_searches:
            del bot.active_searches[user_id]