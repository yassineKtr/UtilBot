from logging import info
import discord
from discord.ext import commands
import youtube_dl

class Music(commands.Cog):
    def __init__(self,client):
        self.client = client
    #join command
    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not connected to a voice channel")
        voice_channel = ctx.author.voice.channel  
        if ctx.voice_client is None:
             await voice_channel.connect() 
        else:
            await ctx.voice_client.move_to(voice_channel)

    #leave command        
    @commands.command()
    async def leave(self,ctx):
       await ctx.voice_client.disconnect()
    

    #play command
    @commands.command()
    async def play(self,ctx,url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url,download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)
    

    @commands.command()
    async def pause(self,ctx):
       ctx.voice_client.pause()
       await ctx.send("Paused...")

    @commands.command()
    async def resume(self,ctx):
       ctx.voice_client.resume()
       await ctx.send("Resumed !!")

    @commands.command()
    async def stop(self,ctx):
        ctx.voice_client.stop()
        await ctx.send("7bes mosi9a")


def setup(client):
        client.add_cog(Music(client))


        

