import discord
from discord.ext import commands
from discord import app_commands
import os
import sys
import asyncio

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_owner(self, interaction: discord.Interaction):
        app = await self.bot.application_info()
        return interaction.user.id == app.owner.id

    @app_commands.command(name="shutdown", description="Éteint le bot.")
    async def shutdown(self, interaction: discord.Interaction):
        if not await self.is_owner(interaction):
            await interaction.response.send_message("Tu n'es pas autorisé à utiliser cette commande.", ephemeral=True)
            return

        await interaction.response.send_message("Arrêt du bot...", ephemeral=True)
        print('Bot off')
        await self.bot.close()

    @app_commands.command(name="restart", description="Redémarre le bot.")
    async def restart(self, interaction: discord.Interaction):
        if not await self.is_owner(interaction):
            await interaction.response.send_message("Tu n'es pas autorisé à utiliser cette commande.", ephemeral=True)
            return

        await interaction.response.send_message("Redémarrage du bot...", ephemeral=True)
        print('Bot is restarting')
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(Admin(bot))