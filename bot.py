import os
import discord
from discord.ext import commands

# Prende i valori dalle variabili d'ambiente
TOKEN = os.getenv('TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', 0))
BAN_REASON = "You have been kicked for posting in a restricted channel"

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
        user = message.author
        
        try:
            # 1. Prova a mandare un DM all'utente
            try:
                dm = await user.create_dm()
                await dm.send(f"**You have been banned** for posting in a restricted channel.")
                print(f"📨 DM inviato a {user.name}")
            except discord.Forbidden:
                print(f"⚠️ Impossible to send a dm to {user.name} (DM closed)")
            except Exception as e:
                print(f"⚠️ Error {user.name}: {e}")
            
            # 2. Banna l'utente
            await user.ban(reason=BAN_REASON)
            print(f"🔨 Bannato {user.name} (ID: {user.id})")
            
            # 3. Messaggio di conferma nel canale (opzionale)
            await message.channel.send(f"🔨 {user.mention} è stato bannato!", delete_after=5)
            
        except discord.Forbidden:
            print(f"Cant ban {user.name}")
            await message.channel.send(f"Cant ban {user.mention}!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    await bot.process_commands(message)

@bot.command()
async def status(ctx):
    """Mostra lo stato del bot"""
    await ctx.send(f"🟢 Bot attivo - Monitoro il canale <#{TARGET_CHANNEL_ID}>")

@bot.command()
@commands.has_permissions(administrator=True)
async def test_dm(ctx, member: discord.Member):
    """Comando di test per verificare l'invio dei DM (solo admin)"""
    try:
        dm = await member.create_dm()
        await dm.send("🧪 Questo è un messaggio di test dal bot!")
        await ctx.send(f"✅ DM inviato a {member.mention}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)
