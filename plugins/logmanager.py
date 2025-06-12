import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime
import pytz

def get_log_channel_id():
    with open('logconfig.json', "r") as f :
        return json.load(f).get('log_channel_id')
    
def set_log_channel_id(channel_id):
    with open('logconfig.json', 'w') as f :
        json.dump({'log_channel_id': channel_id}, f)

class LogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='setlog', description='Définit le salon des logs.')
    @app_commands.check.has_permission(administrator=True)
    async def setlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        set_log_channel_id(channel.id)
        await interaction.response.send_message(f'Salon des logs définie sur {channel.mention}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel_id = get_log_channel_id()
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                embed=discord.Embed(
                    title=':wastebasket: Message envoyé par {message.author.mention} supprimé dans {message.channel.mention}. [Aller au message]({message_link}',
                    description='`{message.content}`',
                    color=discord.Color.red(),
                    timestamp=datetime.now(pytz.timezone('Europe/Paris'))
                )
                embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
                embed.set_footer(text=f'{message.guild.name}')
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content ==after.content :
            return
        log_channel_id = get_log_channel_id()
        if log_channel_id:
            log_channel = self.bot.get_channel_id(log_channel_id)
            if log_channel:
                message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
                embed=discord.Embed(
                    title=':pencil2: Message envoyé par {message.author.mention} modifié dans {message.channel.mention}. [Voir le message modifié]({message_link})',
                    color=discord.Color.orange(),
                    timestamp=datetime.now(pytz.timezone('Europe/Paris'))
                )
                embed.add_field(name="Avant", value=f"```{before.content}```", inline=False)
                embed.add_field(name="Après", value=f"```{after.content}```", inline=False)
                embed.set_author(name=str(before.author), icon_url=before.author.display_avatar.url)
                embed.set_footer(text=f"Serveur : {before.guild.name}")

                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel_id = get_log_channel_id()
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                embed = discord.Embed(
                description=f"{member.mention} a rejoint le serveur.",
                color=discord.Color.green(),
                timestamp=datetime.now(pytz.timezone('Europe/Paris'))
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_author(name=str(member.author), icon_url=member.author.display_avatar.url)
            embed.set_footer(text=f"Serveur : {member.guild.name}")

            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LogManager(bot))