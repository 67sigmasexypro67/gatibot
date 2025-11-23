import discord
from discord.ext import commands
import requests
from gtts import gTTS
import os

# --- TOKEN ve API KEY ---
DISCORD_TOKEN = "YOUR_DISCORD_TOKEN"
LLAMA_KEY = "YOUR_LLAMA_KEY"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Hermes 3 – Llama 3.1 8B API fonksiyonu ---
def ask_hermes(message):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {LLAMA_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "Hermes-3-Llama-3.1-8B",
        "messages": [{"role": "user", "content": message}]
    }
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# --- Yazılı cevap komutu ---
@bot.command()
async def yaz(ctx, *, text):
    cevap = ask_hermes(text)
    await ctx.send(f"🧠 **Hermes:** {cevap}")

# --- Sesli cevap komutu ---
@bot.command()
async def ses(ctx, *, text):
    cevap = ask_hermes(text)
    tts = gTTS(cevap, lang="tr")
    tts.save("reply.mp3")

    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
    ctx.voice_client.play(discord.FFmpegPCMAudio("reply.mp3"))

bot.run(DISCORD_TOKEN)
