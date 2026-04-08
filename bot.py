import discord
from discord.ext import commands

# === CONFIGURAZIONE - MODIFICA QUESTI VALORI! ===
TOKEN = "MTQ5MTQxNTE4NzQ4MjIxODUwNg.GsDPmL.TDUQCHtWdKAkVx5RtEO_Ic7BJnZgjWzFYL-QVI"  # 👈 METTI IL TOKEN VERO!
TARGET_CHANNEL_ID = 1491412208347910194  # 👈 METTI L'ID DEL CANALE VERO!
BAN_REASON = "You have been kicked for posting in a restricted channel."

# Configura il bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")
    print(f"🎯 Monitoraggio canale ID: {TARGET_CHANNEL_ID}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == TARGET_CHANNEL_ID:
        try:
            await message.author.ban(reason=BAN_REASON)
            print(f"🔨 Bannato {message.author.name}")
            await message.channel.send(f"🔨 {message.author.mention} è stato bannato!", delete_after=3)
        except discord.Forbidden:
            print(f"❌ Permessi insufficienti per bannare {message.author.name}")
        except Exception as e:
            print(f"❌ Errore: {e}")
    
    await bot.process_commands(message)

@bot.command()
async def status(ctx):
    """Mostra lo stato del bot"""
    await ctx.send(f"🟢 Bot attivo - Monitoro il canale <#{TARGET_CHANNEL_ID}>")

# Avvia il bot
if __name__ == "__main__":
    bot.run(TOKEN)
