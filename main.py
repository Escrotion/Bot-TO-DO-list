import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        # Pon aquí el ID de tu servidor
        guild = discord.Object(id=700372323844489336)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ {len(synced)} slash commands sincronizados")
    except Exception as e:
        print(f"❌ Error sincronizando comandos: {e}")

async def main():
    async with bot:
        await bot.load_extension("cogs.todo")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())