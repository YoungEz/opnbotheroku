import discord, time, datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.utils import get
import asyncio
import time
import colorsys
import sys
import subprocess
import os
import json
import traceback
import random

import youtube_dl
from discord.utils import find
import requests as rq




bot = commands.Bot(command_prefix='op!')





from discord import opus
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))

opts = {
    'default_search': 'auto',
    'quiet': True,
    "no_warnings":True,
    "simulate":True,
    "nooverwrites":True,
    "keepvideo":False,
    "cachedir":False,
    "noplaylist":True,
    "prefer_ffmpeg":True
}  # youtube_dl options


load_opus_lib()

servers_songs = {}
player_status = {}
now_playing = {}
song_names = {}
paused = {}
rq_channel={}


async def set_player_status():
    for i in bot.servers:
        player_status[i.id] = False
        servers_songs[i.id] = None
        paused[i.id] = False
        song_names[i.id] = []
    print(200)


async def bg():
    bot.loop.create_task(set_player_status())

@bot.event
async def on_ready():
    print ("Bot FF • DW On")
    print ("quem ta falando é o " + bot.user.name)
    print ("Meu numero do ZipZop: " + bot.user.id)
    while True:
    	await bot.change_presence(game=discord.Game(name='Fui criado pelo Mateusᵀᴷ#6548| op!ajuda'.format(len(bot.servers)), type=2))
    	await asyncio.sleep(20)
    	await bot.change_presence(game=discord.Game(name=str(len(set(bot.get_all_members())))+ ' Membros!', type=3))
    	await asyncio.sleep(10)

@bot.event
async def on_voice_state_update(before, after):
    if bot.is_voice_connected(before.server) == True: #bot is connected to voice channel in the server
        # if before.voice.voice_channel == None:
        #     pass
        if before.voice.voice_channel != None: #user in voice channel

            if after.voice.voice_channel!= None and after.voice.voice_channel.id == bot.voice_client_in(before.server).channel.id:
                if player_status[before.server.id]==True:
                    if paused[before.server.id]==True:
                        servers_songs[before.server.id].resume()
                        paused[before.server.id]=False

            if before.voice.voice_channel.id == bot.voice_client_in(before.server).channel.id: # user left the voice channel detected
                if len(bot.voice_client_in(before.server).channel.voice_members) <= 1: #there is only bot in voice channel
                    if player_status[before.server.id]==True:
                        servers_songs[before.server.id].pause()
                        paused[before.server.id]=True
                        await asyncio.sleep(10)
                        if len(bot.voice_client_in(before.server).channel.voice_members) <= 1:
                            await bot.voice_client_in(before.server).disconnect()
                            servers_songs[before.server.id]=None
                            player_status[before.server.id]=False
                            paused[before.server.id]=False
                            now_playing[before.server.id]=None
                            song_names[before.server.id].clear()
                            await bot.send_message(discord.Object(id=rq_channel[before.server.id]),"**Kurusaki left because there was no one inside `{}`**".format(before.voice.voice_channel))






@bot.event
async def on_command_error(con,error):
    pass


async def queue_songs(con, skip, clear):
    if clear == True:
        await bot.voice_client_in(con.message.server).disconnect()
        player_status[con.message.server.id] = False
        song_names[con.message.server.id].clear()

    if clear == False:
        if skip == True:
            servers_songs[con.message.server.id].pause()

        if len(song_names[con.message.server.id]) == 0:
            servers_songs[con.message.server.id] = None

        if len(song_names[con.message.server.id]) != 0:
            r = rq.Session().get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key=AIzaSyDy4gizNmXYWykfUACzU_RsaHtKVvuZb9k'.format(
                song_names[con.message.server.id][0])).json()
            pack = discord.Embed(title=r['items'][0]['snippet']['title'],
                                 url="https://www.youtube.com/watch?v={}".format(r['items'][0]['id']['videoId']))
            pack.set_thumbnail(url=r['items'][0]['snippet']
                               ['thumbnails']['default']['url'])
            pack.add_field(name="Requested by:", value=con.message.author.name)

            song = await bot.voice_client_in(con.message.server).create_ytdl_player(song_names[con.message.server.id][0], ytdl_options=opts, after=lambda: bot.loop.create_task(after_song(con, False, False)))
            servers_songs[con.message.server.id] = song
            servers_songs[con.message.server.id].start()
            await bot.delete_message(now_playing[con.message.server.id])
            msg = await bot.send_message(con.message.channel, embed=pack)
            now_playing[con.message.server.id] = msg

            if len(song_names[con.message.server.id]) >= 1:
                song_names[con.message.server.id].pop(0)

        if len(song_names[con.message.server.id]) == 0 and servers_songs[con.message.server.id] == None:
            player_status[con.message.server.id] = False


async def after_song(con, skip, clear):
    bot.loop.create_task(queue_songs(con, skip, clear))


@bot.command(pass_context=True)
async def play(con, *, url):
    """PLAY THE GIVEN SONG AND QUEUE IT IF THERE IS CURRENTLY SOGN PLAYING"""
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**Você deve está em um canal de texto para usar esse comando.**")

    if con.message.channel.is_private == False: #comand is used in a server
        rq_channel[con.message.server.id]=con.message.channel.id
        if bot.is_voice_connected(con.message.server) == False:
            await bot.join_voice_channel(con.message.author.voice.voice_channel)

        if bot.is_voice_connected(con.message.server) == True:
            if player_status[con.message.server.id] == True:
                song_names[con.message.server.id].append(url)
                r = rq.Session().get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key=put your youtube token here'.format(url)).json()
                await bot.send_message(con.message.channel, "**Song `{}` Queued**".format(r['items'][0]['snippet']['title']))

            if player_status[con.message.server.id] == False:
                player_status[con.message.server.id] = True
                song_names[con.message.server.id].append(url)
                song = await bot.voice_client_in(con.message.server).create_ytdl_player(song_names[con.message.server.id][0], ytdl_options=opts, after=lambda: bot.loop.create_task(after_song(con, False, False)))
                servers_songs[con.message.server.id] = song
                servers_songs[con.message.server.id].start()
                r = rq.Session().get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key=AIzaSyDy4gizNmXYWykfUACzU_RsaHtKVvuZb9k'.format(url)).json()
                pack = discord.Embed(title=r['items'][0]['snippet']['title'],
                                     url="https://www.youtube.com/watch?v={}".format(r['items'][0]['id']['videoId']))
                pack.set_thumbnail(
                    url=r['items'][0]['snippet']['thumbnails']['default']['url'])
                pack.add_field(name="by:",
                               value=con.message.author.name)
                msg = await bot.send_message(con.message.channel, embed=pack)
                now_playing[con.message.server.id] = msg
                song_names[con.message.server.id].pop(0)



@bot.command(pass_context=True)
async def skip(con):
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**Você deve esta em um canal de texto para usar esse comando**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] == None or len(song_names[con.message.server.id]) == 0 or player_status[con.message.server.id] == False:
            await bot.send_message(con.message.channel, "**Nenhuma musica na fila para pular!**")
        if servers_songs[con.message.server.id] != None:
            bot.loop.create_task(queue_songs(con, True, False))

@bot.command(pass_context=True)
async def join(con,*,channel=None):
    """JOIN A VOICE CHANNEL THAT THE USR IS IN OR MOVE TO A VOICE CHANNEL IF THE BOT IS ALREADY IN A VOICE CHANNEL"""


    # COMMAND IS IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**Você deve esta em um canal de texto para usar esse comando**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        voice_status = bot.is_voice_connected(con.message.server)

        voice=find(lambda m:m.name == channel,con.message.server.channels)

        if voice_status == False and channel == None:  # VOICE NOT CONNECTED
            if con.message.author.voice_channel == None:
                await bot.send_message(con.message.channel,"**Você Deve estar em um canal de voz para usar esse comando**")
            if con.message.author.voice_channel != None:
                await bot.join_voice_channel(con.message.author.voice.voice_channel)

        if voice_status == False and channel != None:  # PICKING A VOICE CHANNEL
            await bot.join_voice_channel(voice)

        if voice_status == True:  # VOICE ALREADY CONNECTED
            if voice == None:
                await bot.send_message(con.message.channel, "**Bot conectado ao canal de voz**")


            if voice != None:            
                if voice.type == discord.ChannelType.voice:
                     await bot.voice_client_in(con.message.server).move_to(voice)


@bot.command(pass_context=True)
async def leave(con):
    """LEAVE THE VOICE CHANNEL AND STOP ALL SONGS AND CLEAR QUEUE"""
    # COMMAND USED IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**Você deve estar em um canal de texto para usar esse comando**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:

        # IF VOICE IS NOT CONNECTED
        if bot.is_voice_connected(con.message.server) == False:
            await bot.send_message(con.message.channel, "**Bot desconectado do canal de voz**")

        # VOICE ALREADY CONNECTED
        if bot.is_voice_connected(con.message.server) == True:
            bot.loop.create_task(queue_songs(con, False, True))

@bot.command(pass_context=True)
async def pause(con):
    # COMMAND IS IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**Você deve estar em um canal de voz para usar esse comando**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] != None:
            if paused[con.message.server.id] == True:
                await bot.send_message(con.message.channel, "**A Musica foi pausada**")
            if paused[con.message.server.id] == False:
                servers_songs[con.message.server.id].pause()
                paused[con.message.server.id] = True




@bot.command(pass_context=True)
async def resume(con):
    # COMMAND IS IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**Você deve estar em um canal de voz para usar esse comando**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] != None:
            if paused[con.message.server.id] == False:
                await bot.send_message(con.message.channel, "**Audio ja tocando**")
            if paused[con.message.server.id] == True:
                servers_songs[con.message.server.id].resume()
                paused[con.message.server.id] = False



@bot.command(pass_context=True)
async def volume(con,vol:float):
    if player_status[con.message.server.id] == False:
        await bot.send_message(con.message.channel,"Nenhuma musica no momento")
    if player_status[con.message.server.id] == True:
        servers_songs[con.message.server.id].volume =vol;






	
	




    
@bot.command(pass_context=True)
async def ping(ctx):
	channel = ctx.message.channel
	t1 = time.perf_counter()
	await bot.send_typing(channel)
	t2 = time.perf_counter()
	embed=discord.Embed(title="Pong!", description='Meu Ping {}ms.'.format(round((t2-t1)*1000)), color=0x76FF03)
	embed.set_footer(text ='By: {}| Bot Oficial ØPŇ - Open Night ★'.format(ctx.message.author.name))
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def votar(ctx, *, mensagem: str= None):
	if not mensagem:
		return await bot.say('Você precisa falar algo para votar')
	else:
			vote = await bot.say(embed=discord.Embed(color=0xff0000, description=mensagem))
			await bot.add_reaction(vote, "✅")
			await bot.add_reaction(vote, "❌")
	print('comando votar digitado no servidor {} por {}'.format(ctx.message.server.name, ctx.message.author))
	
@bot.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
	embed = discord.Embed(title="perfil de {}".format(user.name), description="Reflexão: Hoje n tem reflexão :(", color=0x00ff00)
	embed.add_field(name="Nome", value=user.name, inline=True)
	embed.add_field(name="ID do usuário", value=user.id, inline=True)
	embed.add_field(name="Status do usuário", value=user.status, inline=True)
	embed.add_field(name="Melhor cargo", value=user.top_role)
	embed.add_field(name="entrou no servidor", value=user.joined_at)
	embed.set_footer(text ='Comando pedido por: {} | ØPŇ - Open Night ★ Oficial'.format(ctx.message.author.name))
	await bot.say(embed=embed)
	print('comando attlogs digitado no servidor {} por {}'.format(ctx.message.server.name, ctx.message.author))
	
@bot.command(pass_context=True)
async def serverinfo(ctx):
	embed = discord.Embed(name="{}' serverinfo".format(ctx.message.server.name), description="op!ajuda para ver meus comandos!.", color=0x00fA00)
	embed.add_field(name="📄Nome do servidor", value=ctx.message.server.name, inline=True)
	embed.add_field(name = '👑 Dono', value = str(ctx.message.server.owner) + '\n' + ctx.message.server.owner.id);
	embed.add_field(name="💻ID do servidor", value=ctx.message.server.id, inline=True)
	embed.add_field(name="🎓Total de roles", value=len(ctx.message.server.roles), inline=True)
	embed.add_field(name="👥Total de Membros", value=len(ctx.message.server.members))
	embed.add_field(name='🌎 Região', value=ctx.message.server.region)
	embed.add_field(name='👮Role Top1', value=ctx.message.server.role_hierarchy[0])
	embed.set_footer(text ='Comando pedido por: {} | ØPŇ - Open Night ★ Oficial'.format(ctx.message.author.name))
	embed.set_thumbnail(url=ctx.message.server.icon_url)
	await bot.say(embed=embed)
	print('comando serverinfo digitado no servidor {} por {}'.format(ctx.message.server.name, ctx.message.author))
@bot.command(pass_context=True)
async def avatar(ctx, user: discord.User):
	
	list = (user.avatar_url), (user.avatar_url)
	hug = random.choice(list)
	hugemb = discord.Embed(title='Avatar de {}'.format(user.name), color=0x6A1B9A)
	hugemb.set_image(url=hug)
	hugemb.set_footer(text ='Comando pedido por: {} | ØPŇ - Open Night ★ Oficial'.format(ctx.message.author.name))
	await bot.say(embed=hugemb)
	print('comando avatar digitado no servidor {} por {}'.format(ctx.message.server.name, ctx.message.author))
	
@bot.command(pass_context = True)
@commands.has_permissions(ban_members=True)
async def avisar(ctx, member: discord.Member, *, content: str):
	embed = discord.Embed(description='{} foi avisado com sucesso! por {}'.format(member.mention, ctx.message.author.mention), color=0x7a00bb)
	embedpv = discord.Embed(title='Aviso', color=0x00AB70)
	embedpv.add_field(name='Aviso Do servidor', value=ctx.message.server.name)
	embedpv.add_field(name='Autor', value=ctx.message.author)
	embedpv.add_field(name='Motivo', value=content)
	embedpv.set_thumbnail(url=ctx.message.server.icon_url)
	await bot.send_message(member, embed=embedpv)
	
	await bot.say(embed=embed)  
	print('comando avisar digitado no servidor {} por {}'.format(ctx.message.server.name, ctx.message.author))	
	
@bot.command(pass_context=True)
async def addrole(ctx, role: discord.Role, member: discord.Member=None):
    member = member or ctx.message.author
    await bot.add_roles(member, role)
    embed = discord.Embed(description=' ✅Role Adicionada com sucesso!', color=0x00ff00)
    await bot.say(embed=embed)
    print('comando addrole digitado no servidor {} por {}'.format(ctx.message.server.name, ctx.message.author))	


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def removerole(ctx, role: discord.Role, member: discord.Member=None):
    member = member or ctx.message.author
    await bot.remove_roles(member, role)
    embed = discord.Embed(description=' 👮Role removida com sucesso', color=0xff0000)
    await bot.say(embed=embed)
    print('comando removerole digitado no servidor {} por {}'.format(ctx.message.server.name, ctx.message.author))			

									
@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def voicemute(ctx, member: discord.Member):
    await bot.server_voice_state(member,mute=True)
    emb = discord.Embed(title='Usuário mutado voz', description='{} foi mutado com sucesso.'.format(member.mention), color=0xE57373)
    emb.set_footer(text ='Comando pedido por: {} | ØPŇ - Open Night ★ Oficial'.format(ctx.message.author.name))
    await bot.say(embed=emb)
    
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, limit: int=100):
    async for msg in bot.logs_from(ctx.message.channel, limit=limit):
            try:
                await bot.delete_message (msg)
            except:
                pass
    embed = discord.Embed(description="**{}** mensagens apagadas com sucesso! {} :smile:".format(limit, ctx.message.author.mention), color=0x00ff00)
    embed.set_footer(text ='Comando pedido por: {} | ØPŇ - Open Night ★ Oficial'.format(ctx.message.author.name))    																															
@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def voiceunmute(member: discord.Member):
	await bot.server_voice_state(member,mute=False)
	emb = discord.Embed(title='Usuário desmutado voz', description='{} foi desmutado com sucesso.'.format(member.mention), color=0x00ffbb)

	emb.set_footer(text ='Comando pedido por: {} | ØPŇ - Open Night ★ Oficial'.format(ctx.message.author.name))
	await bot.say(embed=emb)    																																																																										
bot.run(str(os.environ.get('BOT_TOKEN')))
