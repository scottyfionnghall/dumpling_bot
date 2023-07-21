import discord
import os
import logging
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from donat_converter import dnt_trnslt
from playlist import playlist
from playlist import playlist_get_dir

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
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
            options = "-loglevel panic"
            after = lambda e: asyncio.run_coroutine_threadsafe(next(ctx), bot.loop)
            player.play(FFmpegPCMAudio(source = song_queue[0], options = options),after=after)
            current_song = {song_queue[0].strip(playlist_get_dir()).removesuffix(".mp3")}
            await ctx.send(f'Playing: {current_song}')
        except:
            await ctx.send(f'Connect to voice channel')
    except:
        await ctx.send(f'Connect to voice channel')

@bot.command()
async def next(ctx):
    if player.is_playing():
        player.stop()
    else:
        try:
            song_queue.pop(0)
            options = "-loglevel panic"
            after = lambda e: asyncio.run_coroutine_threadsafe(next(ctx), bot.loop)
            player.play(FFmpegPCMAudio(source = song_queue[0], options = options),after=after)
            current_song = {song_queue[0].strip(playlist_get_dir()).removesuffix(".mp3")}
            await ctx.send(f'Playing: {current_song}')
        except:
            await ctx.send(f'Connect to voice channel or start playing music')
@bot.command()
async def stop(ctx):
    await ctx.send(f'Stopping ...')
    player.stop()
    await player.disconnect()

@bot.command()
async def pause(ctx):
    await ctx.send(f'Paused ...')
    player.pause()

@bot.command()
async def resume(ctx):
    await ctx.send(f'Resuming ...')
    player.resume()

@bot.command()
async def translate(ctx, *args):
    if args:
        arguments = ' '.join(args)
        await ctx.send(f'Translation: {dnt_trnslt(arguments)}')
    else:
        await ctx.send(f'After the command write text to translate')

bot.run(token, log_handler=handler)
