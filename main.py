import discord
from discord.ext import commands
import requests
from gtts import gTTS
import os

# --- TOKEN ve API KEY ---
DISCORD_TOKEN = "YOUR_DISCORD_TOKEN"
GROK_KEY = "YOUR_GROK_KEY"

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
    cevap = ask_grok(text)
    await ctx.send(f"🧠 **Grok:** {cevap}")

# --- Sesli komut ---
@bot.command()
async def ses(ctx, *, text):
    cevap = ask_grok(text)
    tts = gTTS(cevap, lang="tr")
    tts.save("reply.mp3")

    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
    ctx.voice_client.play(discord.FFmpegPCMAudio("reply.mp3"))

bot.run(DISCORD_TOKEN)
