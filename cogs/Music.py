from logging import info
import discord
from discord.ext import commands
from discord.ext.commands.core import after_invoke
import youtube_dl
from youtube_dl.YoutubeDL import YoutubeDL
from youtubesearchpython import VideosSearch

class Music(commands.Cog):

    

    def __init__(self,client):
        self.client = client

        # music is playing (for the queue) 
        self.is_playing = False

        # arrays of music params
        self.music_queue = [] #[song,channel]
        self.FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS = {'format': "bestaudio",'noplaylist':'True'}
        self.vc = ""


    ########## utility functions 

    # youtube search function
    def search_yt(self,item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %item,download=False)['entries'][0]
            except Exception:
                return False
            return {'source':info['formats'][0]['url'],'title':info['title']}
    
    # play next function
    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            f_url = self.music_queue[0][0]['source']
            
            #remove the first element 
            self.music_queue.pop(0)
           
            self.vc.play(discord.FFmpegPCMAudio(f_url, **self.FFMPEG_OPTIONS),after=lambda e: self.play_next())
        else:
            self.is_playing = False
    
    # the actual play function !
    async def play_music(self):
        if len(self.music_queue)>0:
            self.is_playing =True
            m_url = self.music_queue[0][0]['source']
           
            #trying to connect to voice channel

            if self.vc =="" or not  self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #removing the first element as we are currently playing it
            self.music_queue.pop(0)
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),after=lambda e: self.play_next())
            
            
        else:
            self.is_playing = False

  
    
    ################### commands

    #play command
    @commands.command(pass_context=True)
    async def play(self,ctx,*args):

        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You must be connected to a voice channel !")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song ... please try again with another keyword ")
            else:
                await ctx.send("Added to queue")
                self.music_queue.append([song,voice_channel])

                if self.is_playing ==False:
                    
                    await self.play_music()
                    
                    

    #skip command 
    @commands.command()
    async def skip(self,ctx):
        if self.vc != "":
            self.vc.stop()
            #play the next song in queue if it exists
            
            await self.play_music()
            



        

       
    

    #leave command        
    @commands.command()
    async def leave(self,ctx):
         if ctx.author.voice is None:
            await ctx.send("You're not connected to the voice channel")
         else:
            await ctx.send("Goodbye 👋")
            await ctx.voice_client.disconnect()
    

    
    
   



    #pause command
    @commands.command()
    async def pause(self,ctx):
       ctx.voice_client.pause()
       await ctx.send("Paused ⏸️")
    #resume command
    @commands.command()
    async def resume(self,ctx):
       ctx.voice_client.resume()
       await ctx.send("Resumed ⏯️")

    #stop command
    @commands.command()
    async def stop(self,ctx):
        ctx.voice_client.stop()
        await ctx.send("Stoped ⏹️")


def setup(client):
        client.add_cog(Music(client))


        

