from discord.ext import commands

class Manager(commands.Cog):
    '''Gère les plugins.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Permet de charger un plugin.')
    async def load(self, ctx, plugin: str):
        try:
            await self.bot.load_extension(f'plugins.{plugin}')
            await ctx.send(f'`{plugin}` chargé.')
        except Exception as e:
            await ctx.send(f'Erreur lors du chargement de `{plugin}` : {e}')

    @commands.command(help='Permet de retirer un plugin.')
    async def unload(self, ctx, plugin: str):
        try:
            await self.bot.unload_extension(f'plugins.{plugin}')
            await ctx.send(f'`{plugin}` déchargé.')
        except Exception as e:
            await ctx.send(f'Erreur lors du déchargement de `{plugin}` : {e}')

    @commands.command(help='Permet de recharger un plugin.')
    async def reload(self, ctx, plugin: str):
        try:
            await self.bot.reload_extension(f'plugins.{plugin}')
            await ctx.send(f'`{plugin}` rechargé.')
        except Exception as e:
            await ctx.send(f'Erreur lors du rechargement de `{plugin}` : {e}')

async def setup(bot):
    await bot.add_cog(Manager(bot))
