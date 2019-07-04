import discord, time, datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import nekos
import time
import colorsys
import sys
import subprocess
from pymongo import MongoClient
import os
import pymongo
import json
import traceback
import requests
import datetime
import random
from matematica import taxa

from random import choice

prefix = ["d!" , "D!"]

bot = commands.Bot(prefix, owner_id=497518244165320734)

bot.remove_command("help")
bot.launch_time = datetime.datetime.utcnow()
url = os.environ.get('URL')
mongo = MongoClient(url)
print('Carregando Extensões')
startup_extensions = ["cogs.music", "cogs.newmember"]
n = "Motivo não definido"

class Main_Commands():
    def __init__(self, bot):
        self.bot = bot



@bot.event
async def on_ready():
    print("=================================")
    print("Nome: %s" % bot.user.name)
    print("ID: %s" % bot.user.id)
    print("=================================")
    while True:
        delta_uptime = datetime.datetime.utcnow() - bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=f"AIDS para {str(len(set(bot.get_all_members())))} Membros"))



if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}.{}'.format(type(e).__name__, e)
            print('falha ao carregar extensoes {} . {}'.format(extension, e))
            print(repr(e))
            
@bot.command(pass_context=True, aliases=['latency', 'pong'])
@commands.cooldown(1, 5.0, commands.BucketType.user)
async def ping(ctx):
    '''Find the response time in milliseconds.\n`latency` `pong`'''
    ptime = time.time()
    embed = discord.Embed(Title='Ping', color=0x00FF00)
    embed.add_field(name='Pong!', value='Calculando...')
    embed.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    ping3 = await ctx.send(embed=embed)
    ping2 = time.time() - ptime
    ping1 = discord.Embed(Title='Ping', color=0x00FF00)
    ping1.add_field(name='Pong!', value=f"💻 **Bot** `{int((round(ping2 * 1000)))} ms.`\n 📡 **API** `{int(bot.latency  * 1000)} ms`")
    ping1.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    await ping3.edit(embed=ping1)           
  
    
 
 
 
@bot.command(pass_context=True, aliases=['bi'])
@commands.cooldown(1, 5.0, commands.BucketType.user)
async def botinfo(ctx):
	embed = discord.Embed(color=0x00ffba)
	delta_uptime = datetime.datetime.utcnow() - bot.launch_time
	hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
	minutes, seconds = divmod(remainder, 60)
	days, hours = divmod(hours, 24)	
	embed.add_field(name="**=====Principais Informações=====**", value=f"📆 **Criado Em:** `17:02 2/07/19`\n<:programador:582173369722601522> **Criador:** {ctx.guild.owner} \n<:programando:582173138448547843> **Linguagem Usada:** Python\n<a:discordlove:582176157609492490> **Versão Discord.py:** {discord.__version__}\n❓ **Prefixo:** `kn!`\n<:uptime:582708017049632768> **Estou Online Há: **`{days}` **Dias** `{hours}` **Horas** `{minutes}` **Minutos** `{seconds}` **Segundos**")

	await ctx.send(embed=embed) 
 
@bot.command(pass_context=True)
@commands.cooldown(1, 5.0, commands.BucketType.user)
async def setcargo(ctx, role: discord.Role=None, member: discord.Member=None, *, motivo: str=None):
    if not member:
    	return await ctx.send('{} Você não especificou o usuário.'.format(ctx.message.author.mention))

    	return await ctx.send(embed=rcat)
  
    if not role:
        await ctx.send('{} Você Precisa Mencionar Um Cargo Para Adicionar'.format(ctx.message.author.mention))
    else:
        await member.add_roles(role)
    embed = discord.Embed(title='Ação | Adicionar Cargo', color=0xff0000)
    embed.add_field(name='👮 Autor', value=ctx.message.author)
    embed.add_field(name='💻 Id', value=ctx.message.author.id)
    embed.add_field(name='👥 Usuário', value=member)
    embed.add_field(name='💻 Id', value=member.id)
    
    await ctx.send(embed=embed)

  	


@bot.command(pass_context=True)
@commands.cooldown(1, 5.0, commands.BucketType.user)
async def removercargo(ctx, role: discord.Role=None, member: discord.Member=None, *, motivo: str=None):
    if not member:
    	return await ctx.send('{} Você não especificou o usuário.'.format(ctx.message.author.mention))

    	return await ctx.send(embed=rcat)
    if not role:
        await ctx.send('{} Você Precisa Mencionar Um Cargo Para Remover'.format(ctx.message.author.mention))
    else:
        await member.remove_roles(role)
    embed = discord.Embed(title='Ação | Remover Cargo', color=0xff0000)
    embed.add_field(name='👮 Autor', value=ctx.message.author)
    embed.add_field(name='💻 Id', value=ctx.message.author.id)
    embed.add_field(name='👥 Usuário', value=member)
    embed.add_field(name='💻 Id', value=member.id)
      
    await ctx.send(embed=embed) 
@bot.command(pass_context = True)

@commands.cooldown(1, 5.0, commands.BucketType.user)
async def kick(ctx, user: discord.User=None, *, motivo: str = None):
    motivo = motivo or n
    if not user:
        return await ctx.send('{} Você não especificou o usuário. Exemplo: ``d!kick <@usuário> <motivo>``'.format(ctx.message.author.mention))
    if not ctx.author.guild_permissions.kick_members:
    	rcat = discord.Embed(title='Erro', description='Você Não Tem Permissão Para Executar Esse Comando.', color=0xFF0000)
    	rcat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
    	return await ctx.send(embed=rcat)        
    else:
        await ctx.guild.kick(user)
        embed = discord.Embed(title='Ação | Kick!', description='{} usuário expulso com sucesso'.format(ctx.message.author.mention), color=0xff0Ab)
        embed.add_field(name='👮 Autor', value=ctx.message.author)
        embed.add_field(name='👥 usuário', value=user)
        embed.add_field(name='💻 Id', value=user.id)
        embed.add_field(name='📝 Motivo', value=motivo)
        embed.set_footer(text='Autor do comando: {}| Demon Bot ★'.format(ctx.message.author.name))
        await ctx.send(embed=embed)
        embedpv = discord.Embed(title='Ação | Kick'.format(ctx.message.author.mention), color=0xff0Ab)
        embedpv.add_field(name='👮 Executor', value=ctx.message.author)
        embedpv.add_field(name='💻 Servidor', value=ctx.message.guild.name)
        embedpv.add_field(name='💻 id', value=ctx.message.author.id)
        embedpv.add_field(name='📝 Motivo', value=motivo)
        embedpv.set_thumbnail(url=ctx.message.guild.icon_url)
        await user.send(embed=embedpv)
        

	


@bot.listen("on_command_error")
async def error_handler(ctx, error):
    error = getattr(error, 'original', error)
    cmd_name = ctx.message.content.split()[0]  #pegar nome do cmd com prefixo

    if isinstance(error, commands.CommandOnCooldown):
        s = error.retry_after
        s = round(s, 2)
        h, r = divmod(int(s), 3600)
        m, s = divmod(r, 60)
        return await ctx.send(
            f'{ctx.author.mention} Você terá que aguardar **{str(h) + "h: " if h != 0 else ""}{str(m) + "m: " if m != 0 else ""}{str(s) + "s" if s != 0 else ""}** para usar este comando novamente.')

    if isinstance(error, commands.MissingPermissions):
        perms = "\n".join(error.missing_perms)
        return await ctx.send(f"{ctx.message.author.mention} Você precisa das permissões:\n{perms}\n para usar esse comando").replace('kick_members', 'Expulsar membros').replace('ban_members', 'Banir membros')

    if isinstance(error, commands.BotMissingPermissions):
        perms = "\n".join(error.missing_perms)
        return await ctx.send(f"Não tenho as seguintes permissões:\n{perms}")

    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(f"{ctx.message.author.mention} O comando `{cmd_name}` não foi encontrado em meu sistema. para ver meus comandos digite `d!ajuda`.")



    # Demais erros vão aparecer apenas no console
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
@bot.command(pass_context=True)
async def google(ctx, *, message: str = None):
        try:
            if message is None:
                await ctx.send("Você precisa pesquisar algo! `d!google [pesquisa]`")
            else:
                words = f'https://www.google.com/search?q={message}'.replace(' ', '+')
                search = discord.Embed(title='Pesquisa realizada com sucesso!', description='**Resultado da pesquisa no Google:**', colour=0xff0000, timestamp=datetime.datetime.utcnow())
                search.add_field(name='------------------------------------------------', value=('➡ [RESULTADO](' + words) + ')\n')
                search.set_footer(text='Comando usado pelo(a) {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
                await ctx.send(embed=search)
        except Exception as e:
            await ctx.send(f"[ERROR]: {e}")                 
                       
@bot.command(pass_context=True)
async def i(ctx, cargo: discord.Role):
	await ctx.send(f'{cargo.id}')	
	
@bot.command(pass_context=True, aliases=['tm', 'tempm', 'tmute'])
async def tempmute(ctx, user: discord.Member, temp: int=None):
	role = discord.utils.find(lambda r: r.name == "👮 | Moderador",ctx.author.guild.roles)
		
	if role in ctx.author.roles:
		mt = ctx.guild.get_role(589047230606999553)
		await user.add_roles(mt)		
		s = temp
		s = round(s, 2)
		h, r = divmod(int(s), 3600)
		m, s = divmod(r, 60)
		return await ctx.send(f'{ctx.author.mention} Você silenciou {user.mention} por **{str(h) + "h: " if h != 0 else ""}{str(m) + "m: " if m != 0 else ""}{str(s) + "s" if s != 0 else ""}** com sucesso!')
		await asyncio.sleep(temp)
		await user.remove_roles(mt)
		await user.send('Você aprendeu a falar novamente!')
		
	else:
		await ctx.send(f'{ctx.author.mention} Você precisa do cargo {role.name} para poder usar esse comando')
           
@bot.command(pass_context=True,aliases=['ajuda','h'])
async def help(ctx):
	member = ctx.message.author
	help_p = discord.Embed(color=0xff00AB)
	help_p.add_field(name="Reaja Para Escolher Uma Categoria", value="👮 **Moderação**\n• comandos como `ban, kick...`\nℹ **Informações**\n• comandos como `ping, avatar...`\n🚀 **Outros**\n• comandos como `pergunta, google...``")
	help_p.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')	
	msg = await member.send(embed=help_p)
	await msg.add_reaction('👮')
	await msg.add_reaction('✨')
	await msg.add_reaction('ℹ')
	await msg.add_reaction('🚀')

	
	await ctx.send(f'{member.mention} Verifique Suas Mensagens Privadas.')
	try:
		while True:
			reaction, user = await bot.wait_for("reaction_add", timeout=360, check=lambda reaction, user: reaction.message.id == msg.id and user.id == ctx.author.id)
			emoji = str(reaction.emoji)
			if emoji == '👮':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda Moderação")
				embed_help.add_field(name = 'ban ',value ='Como usar ``d!ban <@usuário> [motivo]`` - bane o usuário mencionado',inline = False)
				embed_help.add_field(name = 'kick',value ='Como usar ``d!kick <@usuário> [motivo]`` - Expulsa o usuário mencionado',inline = False)
				embed_help.add_field(name = 'setcargo',value ='Como usar ``d!setcargo <@cargo> <@usuário>`` - seta um cargo algo usuário mencionado',inline = False)
				embed_help.add_field(name = 'lock',value ='Como usar ``d!lock`` - bloqueia o canal para membros',inline = False)
				embed_help.add_field(name = 'unlock',value ='Como usar ``d!unlock`` - desbloqueia o canal para membros',inline = False)
				embed_help.add_field(name = 'mute',value ='Como usar ``d!mute <@usuário> [motivo]`` - Muta o usuário mencionado **DESATIVADO**',inline = False)
				embed_help.add_field(name = 'unmute',value ='Como usar ``d!unmute <@usuário>`` - Desmuta o usuário mencionado **DESATIVADO**',inline = False)	
				embed_help.add_field(name = 'removercargo',value ='Como usar ``d!removercargo <@cargo> <@usuário>`` - remove um cargo algo usuário mencionado',inline = False)
				embed_help.add_field(name = 'clear',value ='Como usar ``d!clear <quantidade>`` - limpa o canal de texto atual',inline = False)
				embed_help.add_field(name = 'avisar',value ='Como usar ``d!avisar <@usuário> [motivo]`` - avisa uma pessoa sobre algo',inline = False)								
				embed_help.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')												
				msg = await member.send(embed=embed_help)
				await msg.add_reaction('⬅')
			if emoji == '✨':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda Ações", color = 0xff00AA)
				embed_help.add_field(name = 'dance ',value ='Como usar ``s!dance`` - dance com algum usuário',inline = False)
				embed_help.add_field(name = 'kiss',value ='Como usar ``s!kiss <@usuário>`` - O amor esta no ar! beije determinado usuário!',inline = False)
				embed_help.add_field(name = 'hug ',value ='Como usar ``s!hug <@usuário>``',inline = False)
				embed_help.add_field(name = 'suicidio ',value ='Como usar ``s!suicidio``',inline = False)
				embed_help.add_field(name = 'matar',value ='Como usar ``s!matar <@usuário>``',inline = False)
				embed_help.add_field(name = 'slap',value ='Como usar ``s!slap <@usuário>`` -  de uns tap cabuloso em alguem que esta te pertubando',inline = False)
				embed_help.add_field(name = 'chorar ',value ='Como usar ``s!chorar``',inline = False)
				embed_help.add_field(name = 'atack',value ='Como usar ``s!atack <@usuário> - ataque o usuário mencionado``',inline = False)
				embed_help.add_field(name = 'brigar',value ='Como usar ``s!brigar <@usuário>`` - brigue com seu amiguinho (não faça isso)',inline = False)
				embed_help.add_field(name = 'voadora',value ='Como usar ``s!voadora <@usuário>`` - de uma voadora no seu amiguinho (não faça isso)',inline = False)
				embed_help.add_field(name = 'meme',value ='Como usar ``d!meme`` - Mostra Um Meme',inline = False)															
				embed_help.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
				msg = await member.send(embed=embed_help)
				
				await msg.add_reaction('⬅')
			if emoji == 'ℹ':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda Informações", color=0xff00ab)
				embed_help.add_field(name = 'serverinfo',value ='Como usar ``d!serverinfo`` - veja as informações do servidor atual',inline = False)
				embed_help.add_field(name = 'ping',value ='Como usar ``d!ping`` - Veja meu tempo de resposta',inline = False)
				embed_help.add_field(name = 'avatar',value ='Como usar ``d!avatar<@usuário>`` - Veja O Avatar Do Usuário Mencionado',inline = False)
				embed_help.add_field(name = 'ajuda ',value ='Como usar ``d!ajuda`` Meus comandos',inline = False)
				embed_help.add_field(name = 'userinfo',value ='Como usar ``d!userinfo [@usuário]`` Expulsa o usuário mencionado',inline = False)
	
				embed_help.add_field(name = 'google',value ='Como usar ``d!google <pesquisa>`` - Faça Uma Pesquisa',inline = False)
										
				embed_help.set_image(url = 'https://image.ibb.co/caM2BK/help.gif')
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
							
				msg = await member.send(embed=embed_help)
				await msg.add_reaction('⬅')
			if emoji == '🚀':
				await msg.delete()
				embed_help = discord.Embed(description="📙┃Menu de ajuda", color=0xff00ab)
				embed_help.add_field(name = 'dog ',value ='Como usar ``d!dog`` - foto aleatoria de um dogão',inline = False)
				embed_help.add_field(name = 'cat',value ='Como usar ``d!cat`` - foto aleatoria de um gato',inline = False)
				embed_help.add_field(name = 'votar',value ='Como usar ``d!votar <mensagem>`` - Inicie uma votação em seu servidor',inline = False)				
				embed_help.add_field(name = 'flipcoin',value ='Como usar ``flipcoin`` - Cara Ou Coroa',inline = False)																					
				embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
				msg = await member.send(embed=embed_help)
				await msg.add_reaction('⬅')
			if emoji == '💸':
					await msg.delete()
					embed_help = discord.Embed(description="📙┃Menu de Economia", color=0xff00ab)
					embed_help.add_field(name = 'pagar',value ='Como usar ``s!pagar <@usuário> <valor>`` - pague o seu amigo(a) usando minha econimia :)',inline = False)
					embed_help.add_field(name = 'saldo',value ='Como usar ``s!saldo`` - Veja quantos **ryucoins** Você tem!',inline = False)
					embed_help.add_field(name = 'rep',value ='Como usar ``s!rep <@usuário>`` - De um ponto de reputação a alguem',inline = False)
					embed_help.add_field(name = 'reps',value ='Como usar ``s!reps [@usuário]`` - Veja quantos pontos de reputação você (ou seu amigo) tem!',inline = False)
					embed_help.add_field(name = 'daily',value ='Como usar ``s!daily`` - Pegue Uma Recompensa Diaria',inline = False)				
					embed_help.add_field(name = 'Trabalhar',value ='Como usar ``s!trabalhar` - Trabalhe e ganhe ryucoins!',inline = False)
					embed_help.add_field(name="perfil", value="Como Usar ``s!perfil [@usuário]`` Veja seu perfil")
					embed_help.add_field(name="registro", value="Como Usar ``s!registro`` Registre-se em meu sistema")
					embed_help.add_field(name="frase", value="Como Usar ``s!frase <frase>`` Adicione Uma Frase A Seu Perfil")
					embed_help.add_field(name="sobre", value="Como Usar ``s!sobre <desc>` Adicione Uma Descrição a seu perfil")
					embed_help.add_field(name="loja", value="Como Usar ``s!loja`` Veja Meu Shop **(Ainda Não Adicionado)**")
					embed_help.add_field(name="casar", value="Como Usar ``s!casar <@usuário>`` Case com sua webnamorada! **(Ainda Não Adicionado)**")					
					embed_help.add_field(name='-----------------------', value='***<arg> obrigatorio\n[arg] opicional***')				
					msg = await member.send(embed=embed_help)
					await msg.add_reaction('⬅')							
			if emoji == '⬅':
				await msg.delete()
				msg = await member.send(embed=help_p)
				await msg.add_reaction('👮')
				await msg.add_reaction('ℹ')
				await msg.add_reaction('🚀')

	except asyncio.TimeoutError:
		await msg.delete() #deletar mensagem após um tempo sem resposta dos reactions
	except Exception as e:
		await msg.delete()
		print(repr(e))	
		
@bot.command(pass_context=True)
async def dog(ctx):
    '''Check out a random cute or funny dog!'''
    r = requests.get('https://random.dog/woof.json')
    json = r.json()
    if r.status_code == 200:
        sdog = discord.Embed(title='Dogão', color=0x00FF00,timestamp = datetime.datetime.utcnow())
        sdog.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        sdog.set_image(url=json['url'])
        return await ctx.send(embed=sdog)
    else:
        rdog = discord.Embed(title='Error', description='Não pude acessar a API', color=0xFF0000)
        rdog.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rdog)

@bot.command(pass_context=True)
async def cat(ctx):
    '''Check out a random cute or funny cat!'''
    r = requests.get(f'https://catapi.glitch.me/random/')
    json = r.json()
    
    if r.status_code == 200:
        scat = discord.Embed(title='Gato', color=0x00FF00)
        scat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        scat.set_image(url=json['url'])
        scat.set_footer(text=f' {ctx.message.author}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=scat)
    else:
        rcat = discord.Embed(title='Error', description='Não pude accessar a API', color=0xFF0000)
        rcat.set_author(name=f'{ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
        return await ctx.send(embed=rcat)						
                            
bot.run(str(os.environ.get('BOT_TOKEN'))
