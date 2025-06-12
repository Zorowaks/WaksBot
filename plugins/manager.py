import discord
from discord.ext import commands
from discord import app_commands

class PluginManager(app_commands.Group):
    def __init__(self, bot):
        super().__init__(name="plugin", description="Gère les plugins.")
        self.bot = bot

    @app_commands.command(name="load", description="Charge un plugin.")
    @app_commands.describe(plugin="Nom du plugin à charger")
    async def load(self, interaction: discord.Interaction, plugin: str):
        try:
            await self.bot.load_extension(f'plugins.{plugin}')
            await interaction.response.send_message(f"Plugin `{plugin}` chargé avec succès.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors du chargement de `{plugin}` : {e}", ephemeral=True)

    @app_commands.command(name="unload", description="Décharge un plugin.")
    @app_commands.describe(plugin="Nom du plugin à décharger")
    async def unload(self, interaction: discord.Interaction, plugin: str):
        try:
            await self.bot.unload_extension(f'plugins.{plugin}')
            await interaction.response.send_message(f"Plugin `{plugin}` déchargé avec succès.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors du déchargement de `{plugin}` : {e}", ephemeral=True)

    @app_commands.command(name="reload", description="Recharge un plugin.")
    @app_commands.describe(plugin="Nom du plugin à recharger")
    async def reload(self, interaction: discord.Interaction, plugin: str):
        try:
            await self.bot.reload_extension(f'plugins.{plugin}')
            await interaction.response.send_message(f"Plugin `{plugin}` rechargé avec succès.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erreur lors du rechargement de `{plugin}` : {e}", ephemeral=True)

    @app_commands.command(name="list", description="Liste les plugins chargés.")
    async def list(self, interaction: discord.Interaction):
        loaded = list(self.bot.extensions.keys())
        if loaded:
            plugins = "\n".join(f"• `{ext.replace('plugins.', '')}`" for ext in loaded if ext.startswith("plugins."))
            embed = discord.Embed(
                title='Plugin chargé.',
                description=f'\n{plugins}',
                color=discord.Color.purple()
            )
            embed.set_footer(text=interaction.guild.name)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Aucun plugin chargé.", ephemeral=True)


async def setup(bot):
    bot.tree.add_command(PluginManager(bot))