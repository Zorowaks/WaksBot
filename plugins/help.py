import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title='**WaksBot** Help',
            description='Voici toutes les commandes disponibles :',
            color=discord.Color.purple()
        )

        for cog_name, cog in self.bot.cogs.items():
            if cog_name.lower() == 'help':
                continue
            commands_list = cog.get_commands()
            if not commands_list:
                continue
            
            value = ""
            for command in commands_list:
                if command.name == 'help':
                    continue
                value += f'`{command.name}` : {command.help or 'Pas de description'}\n'
            
            embed.add_field(
                name=f'{cog_name} — {cog.__doc__ or 'Aucune description'}',
                value=value,
                inline=False
            )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))