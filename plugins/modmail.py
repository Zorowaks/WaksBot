import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions 
from datetime import datetime
import pytz
import json
import os

ConfigFile = 'data/modmailconfig.json'

def load_modmail_config():
    if not os.path.exists(ConfigFile):
        return{}
    with open(ConfigFile, 'r') as f :
        return json.load(f)

class Modmail(commands.Cog):
    '''Système de messagerie privée avec le staff'''
    def __init__(self, bot):
        self.bot = bot
    
    async def server_autocomplete(self, interaction: discord.Interaction, current: str):
        config = load_modmail_config()
        guilds = [
            guild for guild in self.bot.guilds
            if str(guild.id) in config and guild.get_member(interaction.user.id)
        ]

        return [
            app_commands.Choice(name=guild.name, value=str(guild.id))
            for guild in guilds if current.lower() in guild.name.lower()
        ][:25]

    @app_commands.command(name='modmail', description='Envoyer un ModMail au staff (Uniquement en MP).') 
    @app_commands.describe(server='Serveur sur lequel envoyer le ModMail.', message='contenue du ModMail.')
    @app_commands.autocomplete(server=server_autocomplete)
    async def modmail(self, interaction: discord.Interaction, server: str,  *, message: str):
        if interaction.guild is not None:
            await interaction.response.send_message('Cette commande doit être utilisée en MP', ephemeral=True)
            return
        
        config = load_modmail_config()

        if server not in config:
            await interaction.response.send_message('Serveur non trouvé ou non configuré.', ephemeral=True)
            return
        
        guild = self.bot.get_guild(int(server))
        if not guild:
            await interaction.response.send_message('Aucun serveur trouvé avec le ModMail où vous êtes membre.')
            return
        
        if not guild.get_member(interaction.user.id):
            await interaction.response.send_message("Vous n'êtes pas membre de ce serveur.", ephemeral=True)
            return
        
        channel_id = config[server]
        channel = guild.get_channel(channel_id)
        if not channel:
            await interaction.response.send_message('Erreur : Salon ModMail introuvable.', ephemeral=True)
            return
        
        embed = discord.Embed(
            title='**Nouveau mail reçu.**',
            description=message,
            color=discord.Color(0x1d4ea6),
            timestamp=datetime.now(pytz.timezone('Europe/Paris'))
        )
        embed.set_author(name=str(interaction.user), icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f'ID utilisateur : {interaction.user.id}')

        await channel.send(embed=embed)
        await interaction.response.send_message(f"Ton message a bien été transmis au staff de `{guild.name}` !")

    @has_permissions(manage_messages=True) 
    @app_commands.command(name="reply", description="Permet au staff de repondre au ModMail.")
    @app_commands.describe(user="Utilisateur", reponse='Message')
    async def reply(self, interaction: discord.Interaction, user: discord.User, *, reponse: str):
        try:
            embed=discord.Embed(
                title='**Réponse du staff :**',
                description=f'{reponse}',
                color=discord.Color(0xb56312),
                timestamp=datetime.now(pytz.timezone('Europe/Paris'))
            )
            await user.send(embed=embed)
            await interaction.response.send_message(f'Réponse envoyer à {user.name}.')
        except discord.Forbidden :
            await interaction.response.send_message("Impossible d’envoyer un message à cet utilisateur.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Modmail(bot))