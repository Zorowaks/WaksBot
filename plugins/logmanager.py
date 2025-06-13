import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime
import pytz
from discord.ext.commands import has_permissions
import os

CONFIG_FILE = 'data/logconfig.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_log_channel_id(guild_id):
    config = load_config()
    return config.get(str(guild_id))

def set_log_channel_id(guild_id, channel_id):
    config = load_config()
    config[str(guild_id)] = channel_id
    save_config(config)

class LogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @app_commands.command(name='setlog', description='Définit le salon des logs.')
    @app_commands.describe(channel="Salon où les logs seront envoyés")
    async def setlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not interaction.guild:
            return await interaction.response.send_message("Cette commande doit être utilisée dans un serveur.", ephemeral=True)

        set_log_channel_id(interaction.guild.id, channel.id)
        await interaction.response.send_message(f'Salon des logs défini sur {channel.mention}', ephemeral=True)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return

        log_channel_id = get_log_channel_id(message.guild.id)
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                embed = discord.Embed(
                    description=(f"🗑️ **Message envoyé par {message.author.mention} supprimé dans {message.channel.mention}**.[Voir le message supprimé]({message_link})"),
                    color=discord.Color.red(),
                    timestamp=datetime.now(pytz.timezone('Europe/Paris'))
                )
                embed.add_field(name="Contenu", value=f"```{message.content}```", inline=False)
                embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
                embed.set_footer(text=f"{message.guild.name}")
                await log_channel.send(embed=embed)
 
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content or before.author.bot or not before.guild:
            return

        log_channel_id = get_log_channel_id(before.guild.id)
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
                embed = discord.Embed(
                    description=(f"✏️ **Message envoyé par {before.author.mention} modifié dans {before.channel.mention}.[Voir le message]({message_link})**"),
                    color=discord.Color.orange(),
                    timestamp=datetime.now(pytz.timezone('Europe/Paris'))
                )
                embed.add_field(name="Avant", value=f"```{before.content}```", inline=False)
                embed.add_field(name="Après", value=f"```{after.content}```", inline=False)
                embed.set_author(name=str(before.author), icon_url=before.author.display_avatar.url)
                embed.set_footer(text=f"{before.guild.name}")
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel_id = get_log_channel_id(member.guild.id)
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                embed = discord.Embed(
                    description=f"{member.mention} a rejoint le serveur.",
                    color=discord.Color.green(),
                    timestamp=datetime.now(pytz.timezone('Europe/Paris'))
                )
                embed.set_author(name=str(member), icon_url=member.display_avatar.url)
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f"{member.guild.name}")
                await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LogManager(bot))
