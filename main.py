import discord
from discord.ext import commands
import requests
from gtts import gTTS
import os
import asyncio

# --- TOKEN ve API KEY ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GROK_KEY = os.environ.get("GROK_KEY")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Grok API yazılı cevap ---
def ask_grok(message):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROK_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "grok-4.1-fast",
        "messages": [{"role": "user", "content": message}]
    }
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# --- Yazılı komut ---
@bot.command()
async def yaz(ctx, *, text):
    try:
        cevap = ask_grok(text)
        await ctx.send(f"🧠 **Grok:** {cevap}")
    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

# --- Sesli komut ---
@bot.command()
async def ses(ctx, *, text):
    if ctx.author.voice is None:
        await ctx.send("❌ Ses kanalında değilsin.")
        return

    try:
        cevap = ask_grok(text)
        tts = gTTS(cevap, lang="tr")
        tts.save("reply.mp3")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        ctx.voice_client.play(discord.FFmpegPCMAudio("reply.mp3"))

        # Ses bitene kadar bekle
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        await ctx.voice_client.disconnect()

    except Exception as e:
        await ctx.send(f"❌ Hata: {e}")

bot.run(DISCORD_TOKEN)
