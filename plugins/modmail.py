import discord
from discord.ext import commands
from datetime import datetime
import pytz

class Modmail(commands.Cog):
    '''Système de messagerie privée avec le staff'''
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 1256061641880113193
        self.mail_chanel_id = 1380623091750666321
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild :
            return

        guild =  self.bot.get_guild(self.guild_id)
        mail_channel = guild.get_channel(self.mail_chanel_id)

        if not mail_channel :
            return
        
        embed = discord.Embed(
            title='**Nouveau mail reçu.**',
            description=message.content,
            color=discord.Color(0x1d4ea6),
            timestamp=datetime.now(pytz.timezone('Europe/Paris'))
        )
        embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f'ID utilisateur : {message.author.id}')

        await mail_channel.send(embed=embed)
        await message.channel.send('Ton message a bien été transmis !')

    @commands.command()
    @commands.has_permissions(manage_messages=True) 
    async def reply(self, ctx, user_id: int, *, reponse: str):
        '''Permet au staff de répondre aux messages privés''' 
        user = self.bot.get_user(user_id)
        if user is None :
            try:
                user = await self.bot.fetch_user(user_id)
            except discord.NotFound :
                await ctx.send('Utilisateur introuvable.')
                return
        try:
            embed=discord.Embed(
                title='**Réponse du staff :**',
                description=f'{reponse}',
                color=discord.Color(0xb56312),
                timestamp=datetime.now(pytz.timezone('Europe/Paris'))
            )
            await user.send(embed=embed)
            await ctx.send(f'Réponse envoyer à {user.name}.')
        except discord.Forbidden :
            await ctx.send("Impossible d’envoyer un message à cet utilisateur.")

async def setup(bot):
    await bot.add_cog(Modmail(bot))