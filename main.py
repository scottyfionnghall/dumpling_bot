import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from donat_converter import dnt_trnslt
from playlist import playlist
from playlist import playlist_get_dir

load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    print("Dumpling Bot is Up and Running")

@bot.command()
async def play(ctx):
    global song_queue
    song_queue = playlist()
    try:
        channel = ctx.author.voice.channel
        global player
        try:
            player = await channel.connect()
        except:
            pass
        player.play(FFmpegPCMAudio(song_queue[0]))
        await ctx.send(f'Playing: {song_queue[0].strip(playlist_get_dir())}')
    except:
         await ctx.send(f'Connect to voice channel')

@bot.command()
async def next(ctx):
    try:
        player.stop()
        song_queue.pop(0)
        player.play(FFmpegPCMAudio(song_queue[0]))
        await ctx.send(f'Playing: {song_queue[0].strip(playlist_get_dir())}')
    except:
        await ctx.send(f'Connect to voice channel or start playing music')
@bot.command()
async def stop(ctx):
    song_queue = playlist()
    await ctx.send(f'Stopping ...')
    player.stop()
    await player.disconnect()

@bot.command()
async def pause(ctx):
    await ctx.send(f'Music paused')
    player.pause()

@bot.command()
async def resume(ctx):
    await ctx.send(f'Resuming playing music')
    player.resume()

@bot.command()
async def translate(ctx, *args):
    if args:

        arguments = ' '.join(args)
        await ctx.send(f'Translation: {dnt_trnslt(arguments)}')
    else:
        await ctx.send(f'After the command write text to translate')

bot.run(token)