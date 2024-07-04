# utils/formatters.py

import discord
import validators
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

max_content_length = 200

def create_embed(script, page, total_pages):
    def format_datetime(dt_str):
        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        delta = relativedelta(now, dt)
        
        if delta.years > 0:
            time_ago = f"{delta.years} years ago"
        elif delta.months > 0:
            time_ago = f"{delta.months} months ago"
        elif delta.days > 0:
            time_ago = f"{delta.days} days ago"
        elif delta.hours > 0:
            time_ago = f"{delta.hours} hours ago"
        elif delta.minutes > 0:
            time_ago = f"{delta.minutes} minutes ago"
        else:
            time_ago = "just now"
        
        formatted_date = dt.strftime("%m/%d/%Y | %I:%M:%S %p")
        return f"{time_ago} | {formatted_date}"
    
    game_name = script["game"]["name"]
    game_id = script["game"]["gameId"]
    title = script["title"]
    script_type = script["scriptType"]
    script_content = script["script"]
    views = script["views"]
    verified = script["verified"]
    has_key = script.get("key", False)
    key_link = script.get("keyLink", "")
    is_patched = script.get("isPatched", False)
    is_universal = script.get("isUniversal", False)
    created_at = format_datetime(script["createdAt"])
    updated_at = format_datetime(script["updatedAt"])
    game_image_url = "https://scriptblox.com" + script["game"].get("imageUrl", "")
    slug = script["slug"]

    paid_or_free = "Free" if script_type == "free" else "💲 Paid"
    verified_status = "✅ Verified" if verified else "❌ Not Verified"
    key_status = f"[Key Link]({key_link})" if has_key and key_link else ("🔑 Has Key" if has_key else "✅ No Key")
    patched_status = "❌ Patched" if is_patched else "✅ Not Patched"
    universal_status = "🌐 Universal" if is_universal else "Not Universal"
    truncated_script_content = (script_content[:max_content_length - 3] + "..." if len(script_content) > max_content_length else script_content)

    embed = discord.Embed(title=title, color=0x206694)

    embed.add_field(name="Game", value=f"[{game_name}](https://www.roblox.com/games/{game_id})", inline=True)
    embed.add_field(name="Verified", value=verified_status, inline=True)
    embed.add_field(name="ScriptType", value=paid_or_free, inline=True)
    embed.add_field(name="Universal", value=universal_status, inline=True)
    embed.add_field(name="Views", value=f"👁️ {views}", inline=True)
    embed.add_field(name="Key", value=key_status, inline=True)
    embed.add_field(name="Patched", value=patched_status, inline=True)
    embed.add_field(name="Links", value=f"[Raw Script](https://rawscripts.net/raw/{slug}) - [Script Page](https://scriptblox.com/script/{slug})", inline=False)
    embed.add_field(name="The Script", value=f"```lua\n{truncated_script_content}\n```", inline=False)
    embed.add_field(name="Timestamps", value=f"**Created At:** {created_at}\n**Updated At:** {updated_at}", inline=False)

    set_image_or_thumbnail(embed, game_image_url)

    embed.set_footer(text=f"Made by AdvanceFalling Team | Powered by Scriptblox", #  Page {page}/{total_pages}
                     icon_url="https://img.getimg.ai/generated/img-u1vYyfAtK7GTe9OK1BzeH.jpeg")

    return embed

def set_image_or_thumbnail(embed, url):
    try:
        if url and validators.url(url):
            embed.set_image(url=url)
        else:
            embed.set_image(url="https://c.tenor.com/jnINmQlMNbsAAAAC/tenor.gif")
    except Exception as e:
        print(f"Error setting image URL: {e}")
        embed.set_image(url="https://c.tenor.com/jnINmQlMNbsAAAAC/tenor.gif")