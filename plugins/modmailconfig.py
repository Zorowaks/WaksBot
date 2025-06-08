import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions 
import os
import json

ModMail_File = "modmailconfig.json"

def load_modmail_config(ModMail_File):
    if not os.path.exists(ModMail_File):
        return{}
    with open(ModMail_File, 'r') as f :
        return json.load(f)
    
def save_modmail_config(config):
    with open(ModMail_File, 'w') as f :
        json.dump(config, f, indent=4)

class ModMailConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @app_commands.command(name="setmodmail", description="Configure le channel où seront envoyé les ModMail.")
    @app_commands.describe(channel='channel')
    async def setmodmail(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = load_modmail_config(ModMail_File)
        config[str(interaction.guild.id)] = channel.id
        save_modmail_config(config)
        await interaction.response.send_message(f'Salon ModMail défini sur {channel.mention}')
    
async def setup(bot):
    await bot.add_cog(ModMailConfig(bot))