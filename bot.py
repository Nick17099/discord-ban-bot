import os
import discord
from discord.ext import commands

# ⚠️ NON scrivere il token qui! Lo prende dalle variabili d'ambiente
TOKEN = os.getenv('TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', 0))
BAN_REASON = "You have been kicked for posting in a restricted channel."

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == TARGET_CHANNEL_ID:
        try:
            await message.author.ban(reason=BAN_REASON)
            print(f"🔨 Bannato {message.author.name}")
        except Exception as e:
            print(f"❌ Errore: {e}")
    
    await bot.process_commands(message)

@bot.command()
async def status(ctx):
    await ctx.send(f"🟢 Bot attivo - Monitoro <#{TARGET_CHANNEL_ID}>")

if __name__ == "__main__":
    bot.run(TOKEN)
