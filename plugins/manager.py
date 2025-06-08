import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions 

class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @app_commands.command(name="load", description="Charge un plugin.")
    @app_commands.describe(plugin='plugin')
    async def load(self, interaction: discord.Interaction , plugin: str):
        try:
            await self.bot.load_extension(f'plugins.{plugin}')
            await self.bot.tree.sync()
            await interaction.response.send_message(f'`{plugin}` chargé.', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'Erreur lors du chargement de `{plugin}` : {e}', ephemeral=True)

    @has_permissions(administrator=True)
    @app_commands.command(name="unload", description="Retire un plugin.")
    @app_commands.describe(plugin='plugin')
    async def unload(self, interaction: discord.Interaction, plugin: str):
        try:
            await self.bot.unload_extension(f'plugins.{plugin}')
            await interaction.response.send_message(f'`{plugin}` déchargé.', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'Erreur lors du déchargement de `{plugin}` : {e}', ephemeral=True)

    @has_permissions(administrator=True)
    @app_commands.command(name="reload", description="Recharge un plugin.")
    @app_commands.describe(plugin='plugin')
    async def reload(self, interaction: discord.Interaction, plugin: str):
        try:
            await self.bot.reload_extension(f'plugins.{plugin}')
            await interaction.response.send_message(f'`{plugin}` rechargé.', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'Erreur lors du rechargement de `{plugin}` : {e}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Manager(bot))
