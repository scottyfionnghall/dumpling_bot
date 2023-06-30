import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
from dotenv import load_dotenv
from cmds.donat_converter import dnt_trnslt
load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print("Dumpling Bot is Up and Running")

@bot.command(aliases=['p', 'pla'])
async def play(ctx, args):
    channel = ctx.author.voice.channel
    print(channel)
    global player
    if channel:
        try:
            player = await channel.connect()
        except:
            pass    
        player.play(FFmpegPCMAudio(args))
    else:
        await ctx.send(f'Подключитесь к голосовому каналу')

@bot.command(aliases=['s', 'sto'])
async def stop(ctx):
    player.stop()

@bot.command()
async def translate(ctx, *args):
    if args:
        arguments = ' '.join(args)
        await ctx.send(f'Перевод: {dnt_trnslt(arguments)}')
    else:
        await ctx.send(f'Напишите после комманды текст для перевода')


bot.run(token)