 # Copyright 2021
#This program is free software: you can redistribute it and/or modify
  #  it under the terms of the GNU General Public License as published by
  #  the Free Software Foundation, either version 3 of the License, or
  #  (at your option) any later version.

 #   This program is distributed in the hope that it will be useful,
   # but WITHOUT ANY WARRANTY; without even the implied warranty of
  #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.
#
 #   You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    

 #!./.venv/bin/python

import discord    
import code         
import os           
import inspect      
import random
import os
import argparse
from discord.channel import VoiceChannel       

from discord.ext import commands    




def log_msg(msg: str, level: str):
   
    dsp_sel = {
        'debug'   : ('\033[34m', '-'),
        'info'    : ('\033[32m', '*'),
        'warning' : ('\033[33m', '?'),
        'error'   : ('\033[31m', '!'),
    }

    
    _extra_ansi = {
        'critical' : '\033[35m',
        'bold'     : '\033[1m',
        'unbold'   : '\033[2m',
        'clear'    : '\033[0m',
    }

    
    caller = inspect.stack()[1]

    
    if level not in dsp_sel:
        print('%s%s[@] %s:%d %sBad log level: "%s"%s' % \
            (_extra_ansi['critical'], _extra_ansi['bold'],
             caller.function, caller.lineno,
             _extra_ansi['unbold'], level, _extra_ansi['clear']))
        return

    
    print('%s%s[%s] %s:%d %s%s%s' % \
        (_extra_ansi['bold'], *dsp_sel[level],
         caller.function, caller.lineno,
         _extra_ansi['unbold'], msg, _extra_ansi['clear']))



song_list = {
    'Legendele.mp3' : '1',
    'UUU.mp3' : '2',
    'Umar la Umar.mp3' : '3',
    'Ploaie Divina.mp3' : '4',
    'Arabete.mp3' : '5'
   
}


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    log_msg('logged on as <%s>' % bot.user, 'info')

@bot.event
async def on_message(msg):
   
    if msg.author == bot.user:
        return
    
    log_msg('message from <%s>: "%s"' % (msg.author, msg.content), 'debug')

   
    await bot.process_commands(msg)
    

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return 
    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()

@bot.command(brief='BAGA UNA DE JALE MAIESTRE')
# play - play music
async def play(ctx,song):
    if not ctx.message.author.voice:
        await ctx.send("{} NU ESTI PE CANAL ".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await ctx.send("PREZENT")
        await channel.connect()
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client
            if song in song_list:
                async with ctx.typing():
                    voice_channel.play(discord.FFmpegPCMAudio(song))
                await ctx.send('**Now playing: **' + song)
            else :
                await ctx.send("NU E IN PLAYLIST ")
        except :
            await ctx.send("NIMIC MOMENTAN")

@bot.command()
async def list(ctx):
    await ctx.send("The list is:")
    for key in song_list:
        await ctx.send (song_list[key] + '.' + key)


    

    

@bot.command(brief='LEAVE')
async def scram(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("Te am pupat")
    else:
        await ctx.send("nu sunt cu tine pe canal")


@bot.command(brief='Pause the music')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Pauza")
    else:
        await ctx.send("nimic pe moment")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("rapapaam")
    else:
        await ctx.send("rulez ceva acm")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild= ctx.guild)
    voice.stop();        




# roll - rng chat command
#   @ctx     : command invocation context
#   @max_val : upper bound for number generation (must be at least 1)
@bot.command(brief='Generate random number between 1 and <arg>')
async def roll(ctx, max_val: int):
    # argument sanity check
    if max_val < 1:
        raise Exception('argument <max_val> must be at least 1')

    await ctx.send(random.randint(1, max_val))

# roll_error - error handler for the <roll> command
#   @ctx     : command that crashed invocation context
#   @error   : ...
@roll.error
async def roll_error(ctx, error):
    await ctx.send(str(error))



################################################################################
############################# PROGRAM ENTRY POINT ##############################
################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--token",help="Add token")
    args=parser.parse_args()
    if args.token:
      BOT_TOKEN=args.task
      bot.run(BOT_TOKEN)
    else :
        # check that token exists in environment
        if 'BOT_TOKEN' not in os.environ:
            log_msg('save your token in the BOT_TOKEN env variable!', 'error')
            exit(-1)
        # launch bot (blocking operation)
        bot.run(os.environ['BOT_TOKEN'])
    

