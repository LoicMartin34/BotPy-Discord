import discord
from discord.ext import commands

import random
import asyncio
import youtube_dl

musics = {}
ytdl = youtube_dl.YoutubeDL()

def setup(bot):
    bot.add_cog(Musiques(bot))

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download = False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

class Musiques(commands.Cog):
    """Liste des commandes pour la musique"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leave(self, ctx):
        client = ctx.guild.voice_client
        await client.disconnect()
        musics[ctx.guild] = []

    @commands.command()
    async def pause(self, ctx):
        client = ctx.guild.voice_client
        if not client.is_paused():
            client.pause()

    @commands.command()
    async def resume(self, ctx):
        client = ctx.guild.voice_client
        if client.is_paused():
            client.resume()

    @commands.command()
    async def skip(self, ctx):
        client = ctx.guild.voice_client
        client.stop()

    def play_song(self, client, musicsList, song):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, 
        before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

        def next(_):
            if len(musicsList) > 0:
                newMusic = musicsList[0]
                del musicsList[0]
                self.play_song(client, musicsList, newMusic)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)
        
        client.play(source, after = next)

    @commands.command()
    async def play(self, ctx, url):
        client = ctx.guild.voice_client
        if client and client.channel:
            video = Video(url)
            musics[ctx.guild].append(video)
        else:
            channel = ctx.author.voice.channel
            video = Video(url)
            musics[ctx.guild] = []
            client = await channel.connect()
            await ctx.send(f"Je lance : {video.url}")
            self.play_song(client, musics[ctx.guild], video)
