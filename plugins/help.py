import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche la liste des commandes disponibles triées par plugin.")
    @app_commands.describe(command="Nom d'une commande (ex: remind)")
    async def help(self, interaction: discord.Interaction, command: str = None):
        if command is None:
            embed = discord.Embed(
                title="**WaksBot** help",
                description="Voici la liste des commandes disponibles de **WaksBot**.",
                color=discord.Color.purple()
            )

            for cog_name, cog in self.bot.cogs.items():
                cmds = [f"`/{cmd.qualified_name}`" for cmd in cog.get_app_commands() if cmd.qualified_name != "help"]
                if cmds:
                    embed.add_field(name=cog_name, value=", ".join(cmds), inline=False)

            plugin_group = next((cmd for cmd in self.bot.tree.get_commands() if cmd.name == "plugin"), None)
            if plugin_group and isinstance(plugin_group, app_commands.Group):
                subcommands = [f"`/{cmd.qualified_name}`" for cmd in plugin_group.walk_commands()]
                if subcommands:
                    embed.add_field(name="Plugin", value=", ".join(subcommands), inline=False)

            embed.set_footer(text="Utilise /help <commande> pour plus d’infos.")
            await interaction.response.send_message(embed=embed)

        else:
            search = command.lower()
            for cmd in self.bot.tree.walk_commands():
                if cmd.qualified_name == search:
                    embed = discord.Embed(
                        title=f"Aide pour `/{cmd.qualified_name}`",
                        description=cmd.description or "Aucune description.",
                        color=discord.Color.purple()
                    )
                    if cmd.parameters:
                        params = "\n".join(f"• `{p.name}`: {p.description or 'Pas de description'}" for p in cmd.parameters)
                        embed.add_field(name="Arguments", value=params, inline=False)
                    await interaction.response.send_message(embed=embed)
                    return

            await interaction.response.send_message(f"Commande `/`{search}` introuvable.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
