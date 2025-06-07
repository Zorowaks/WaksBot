import discord
from discord.ext import commands
from datetime import datetime
import pytz
import json
import os

ConfigFile = 'modmailconfig.json'

def load_modmail_config():
    if not os.path.exists(ConfigFile):
        return{}
    with open(ConfigFile, 'r') as f :
        return json.load(f)

class Modmail(commands.Cog):
    '''Système de messagerie privée avec le staff'''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild :
            return

        config = load_modmail_config()
        guild = [
            guild for guild in self.bot.guilds
            if str(guild.id) in config and guild.get_member(message.author.id)
        ]

        if not guild :
            await message.channel.send('Aucun serveur trouvé avec ModMail où vous êtes membre.')
            return

        if len(guild) > 1 :
            text = '**Sur quel serveur souhaitez vous envoyer votre message ?** \n'
            for i, g in enumerate(guild, 1):
                text += f'{i}.{g.name}\n'
            await message.channel.send(text)

            def check(m):
                return m.author == message.author and m.content.isdigit()
                
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=30)
                index = int(reply.content) - 1
                guild = guild[index]

            except:
                message.channel.send('Délai dépassé ou réponse invalide')
                return
        else:
            guild = guild[0]

        channel_id = config[str(guild.id)]
        channel = guild.get_channel(channel_id)
        if not channel :
            await message.channel.send('Erreur : Salon ModMail introuvable')
        
        embed = discord.Embed(
            title='**Nouveau mail reçu.**',
            description=message.content,
            color=discord.Color(0x1d4ea6),
            timestamp=datetime.now(pytz.timezone('Europe/Paris'))
        )
        embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f'ID utilisateur : {message.author.id}')

        await channel.send(embed=embed)
        await message.channel.send('Ton message a bien été transmis !')

    @commands.command()
    @commands.has_permissions(manage_messages=True) 
    async def reply(self, ctx, user_id: int, *, reponse: str):
        '''Permet au staff de répondre aux messages privés''' 
        user = self.bot.get_user(user_id)
        if user is None :
            try:
                user = await self.bot.fetch_user(user_id)
            except discord.NotFound :
                await ctx.send('Utilisateur introuvable.')
                return
        try:
            embed=discord.Embed(
                title='**Réponse du staff :**',
                description=f'{reponse}',
                color=discord.Color(0xb56312),
                timestamp=datetime.now(pytz.timezone('Europe/Paris'))
            )
            await user.send(embed=embed)
            await ctx.send(f'Réponse envoyer à {user.name}.')
        except discord.Forbidden :
            await ctx.send("Impossible d’envoyer un message à cet utilisateur.")

async def setup(bot):
    await bot.add_cog(Modmail(bot))