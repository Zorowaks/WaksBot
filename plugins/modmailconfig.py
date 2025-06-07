import discord
from discord.ext import commands
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

    @commands.command(help='Permet de configurer le salon où les messages ModMail seront envoyés.')
    @commands.has_permissions(administrator=True)
    async def setmodmail(self, ctx, channel: discord.TextChannel):
        config = load_modmail_config(ModMail_File)
        config[str(ctx.guild.id)] = channel.id
        save_modmail_config(config)
        await ctx.send(f'Salon ModMail défini sur {channel.mention}')
    
async def setup(bot):
    await bot.add_cog(ModMailConfig(bot))