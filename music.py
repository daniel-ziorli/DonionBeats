import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import time
import threading

class Song():
    def __init__(self, title, source):
        self.title = title
        self.source = source
        self.voice_client = None


class SongQueue():
    def __init__(self):
        self.queue = []
        self.currently_playing = None

    def addSong(self, song):
        return self.queue.append(song)

    def nextSong(self):
        if self.isEmpty():
            return None
        self.currently_playing = self.queue.pop(0)
        return self.currently_playing

    def removeSong(self, index):
        return self.queue.pop(index)

    def isEmpty(self):
        return len(self.queue) == 0

    def getLength(self):
        return len(self.queue)

    def __str__(self):
        if self.isEmpty():
            return "Queue is empty bimbo"

        out = "\n\n Current Queue:"

        i = 1
        for song in self.queue:
            out += "\n" + str(i) + ". " + song.title
            i += 1

        return out


class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = 'https://www.youtube.com/'
        self.music_queue = SongQueue()
        self.ctx = None
        self.inactivity_timeout = 5

        self.playingQueue = False
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.YDL_OPTIONS = {'format': 'bestaudio'}

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await self.send(ctx, "You're not in the channel cunt")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is None:
            return

        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *url):
        await self.join(ctx)
        url = ' '.join([str(elem) for elem in url])
        if len(url) == 0:
            await self.resume(ctx)
            return

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = None
            print(url[:len(self.prefix)])
            if len(url) < len(self.prefix) or url[:len(self.prefix)] != self.prefix:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)[
                    'entries'][0]
            else:
                try:
                    info = ydl.extract_info(url, download=False)
                except:
                    await self.send(ctx, "Cant find the video you chimp")
                    return

            source = await discord.FFmpegOpusAudio.from_probe(info['formats'][0]['url'], **self.FFMPEG_OPTIONS)
            self.music_queue.addSong(Song(info['title'], source))

            msg = ""
            if self.music_queue.currently_playing is None:
                msg = "Playing: " + str(info['title'])
            else:
                msg = "Queued: " + str(info['title'])
                msg += str(self.music_queue)

            await self.send(ctx, msg)

            if self.music_queue.currently_playing is None:
                thread = threading.Thread(target=self.startPlaying, args=[ctx])
                thread.daemon = True
                thread.start()

    def startPlaying(self, ctx):
        while not self.music_queue.isEmpty() or ctx.voice_client.is_playing():
            if ctx.voice_client.is_playing():
                time.sleep(1)
            else:
                print("next song")
                song = self.music_queue.nextSong()
                ctx.voice_client.play(song.source)

        self.music_queue.currently_playing = None

    @commands.command()
    async def skip(self, ctx):
        if not ctx.voice_client.is_playing():
            return

        if self.music_queue.isEmpty():
            return

        ctx.voice_client.stop()

        if self.music_queue.currently_playing is None:
            thread = threading.Thread(target=self.startPlaying, args=[ctx])
            thread.daemon = True
            thread.start()
        while not ctx.voice_client.is_playing():
            time.sleep(1)

        msg = "Playing: " + self.music_queue.currently_playing.title
        if not self.music_queue.isEmpty():
            msg += str(self.music_queue)
        await self.send(ctx, msg)

    @commands.command()
    async def stop(self, ctx):
        if not ctx.voice_client.is_playing():
            return

        ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            return

        self.ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            return

        ctx.voice_client.resume()

    @commands.command()
    async def queue(self, ctx):
        msg = "Playing: " + self.music_queue.currently_playing.title
        msg += str(self.music_queue)
        await self.send(ctx, msg)

    @commands.command()
    async def remove(self, ctx, index):
        index = int(index) - 1
        if index > self.music_queue.getLength() or index < 0:
            await self.send(ctx, "Number isnt in the queue learn to read")
            return
        
        msg = "Removed: " + self.music_queue.removeSong(index).title
        msg += str(self.music_queue)
        await self.send(ctx, msg)

    async def send(self, ctx, msg):
        await ctx.send("```" + msg + "```")


def setup(client):
    client.add_cog(music(client))
