import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions 

class Manager(commands.Cog):
    '''Gère les plugins.'''
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @app_commands.command(name="load", description="Charge un plugin.")
    @app_commands.describe(plugin='plugin')
    async def load(self, interaction: discord.Interaction , plugin: str):
        try:
            await self.bot.load_extension(f'plugins.{plugin}')
            await self.bot.tree.sync()
            await interaction.response.send_message(f'`{plugin}` chargé.')
        except Exception as e:
            await interaction.response.send_message(f'Erreur lors du chargement de `{plugin}` : {e}')

    @has_permissions(administrator=True)
    @app_commands.command(name="unload", description="Retire un plugin.")
    @app_commands.describe(plugin='plugin')
    async def unload(self, interaction: discord.Interaction, plugin: str):
        try:
            await self.bot.unload_extension(f'plugins.{plugin}')
            await interaction.response.send_message(f'`{plugin}` déchargé.')
        except Exception as e:
            await interaction.response.send_message(f'Erreur lors du déchargement de `{plugin}` : {e}')

    @has_permissions(administrator=True)
    @app_commands.command(name="reload", description="Recharge un plugin.")
    @app_commands.describe(plugin='plugin')
    async def reload(self, interaction: discord.Interaction, plugin: str):
        try:
            await self.bot.reload_extension(f'plugins.{plugin}')
            await interaction.response.send_message(f'`{plugin}` rechargé.')
        except Exception as e:
            await interaction.response.send_message(f'Erreur lors du rechargement de `{plugin}` : {e}')

async def setup(bot):
    await bot.add_cog(Manager(bot))
