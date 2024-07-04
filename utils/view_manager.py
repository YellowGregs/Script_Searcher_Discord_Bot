import discord
import asyncio
from utils.formatters import create_embed

async def display_scripts(ctx, message, scripts, page, total_pages, prefix, bot):
    while True:
        script = scripts[page - 1]
        embed = create_embed(script, page, total_pages)

        view = discord.ui.View()

        if total_pages > 1:
            if page > 1:
                view.add_item(discord.ui.Button(label="⏪", style=discord.ButtonStyle.primary, custom_id="first"))
                view.add_item(discord.ui.Button(label="◀️", style=discord.ButtonStyle.primary, custom_id="previous"))
            view.add_item(discord.ui.Button(label=f"Page {page}/{total_pages}", style=discord.ButtonStyle.secondary, disabled=True))
            if page < total_pages:
                view.add_item(discord.ui.Button(label="▶️", style=discord.ButtonStyle.primary, custom_id="next"))
                view.add_item(discord.ui.Button(label="⏩", style=discord.ButtonStyle.primary, custom_id="last"))
            
            download_url = f"https://scriptblox.com/download/{script['_id']}"
            view.add_item(discord.ui.Button(label="Download", url=download_url, style=discord.ButtonStyle.link))
            
            post_url = f"https://scriptblox.com/script/{script['slug']}"
            view.add_item(discord.ui.Button(label="View", url=post_url, style=discord.ButtonStyle.link))
            
        await message.edit(embed=embed, view=view)

        def check(interaction):
            return interaction.user == ctx.author and interaction.message.id == message.id

        try:
            interaction = await bot.wait_for("interaction", check=check, timeout=30.0)
            if interaction.data["custom_id"] == "previous" and page > 1:
                page -= 1
            elif interaction.data["custom_id"] == "next" and page < total_pages:
                page += 1
            elif interaction.data["custom_id"] == "last":
                page = total_pages
            elif interaction.data["custom_id"] == "first":
                page = 1

            await interaction.response.defer()

        except asyncio.TimeoutError:
            if prefix:
                timeout_message = await ctx.send("You took too long to interact.")
                await asyncio.sleep(5)
                await timeout_message.delete()
            else:
                await ctx.send("You took too long to interact.", ephemeral=True)
            break