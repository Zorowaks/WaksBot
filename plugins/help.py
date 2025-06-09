import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche la liste des commandes disponible.")
    @app_commands.describe(command="Nom d'une commande")
    async def help(self, interaction: discord.Interaction, command: str = None):
        if command is None:
            embed = discord.Embed(
                title="Aide - Commandes disponibles",
                description="Voici la liste des commandes disponibles, triées par plugin.",
                color=discord.Color.purple()
            )

            for cog_name, cog in self.bot.cogs.items():
                command_list = [cmd.name for cmd in cog.get_app_commands() if cmd.name != "help"]
                if command_list:
                    embed.add_field(
                        name=f"{cog_name}",
                        value=", ".join(f"`/{cmd}`" for cmd in command_list),
                        inline=False
                    )
            embed.set_footer(text="Utilise /help <commande> pour plus d’infos.")
            await interaction.response.send_message(embed=embed)
        else:
            for cmd in self.bot.tree.get_commands():
                if cmd.name == command:
                    embed = discord.Embed(
                        title=f"Aide pour /{cmd.name}",
                        description=cmd.description or "Aucune description.",
                        color=discord.Color.purple()
                    )
                    if cmd.parameters:
                        params = "\n".join(f"• `{p.name}`: {p.description or 'Pas de description'}" for p in cmd.parameters)
                        embed.add_field(name="Arguments", value=params, inline=False)
                    await interaction.response.send_message(embed=embed)
                    return
            await interaction.response.send_message(f"Commande `/`{command}` introuvable.`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))