import discord
from discord.ext import commands
import json
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!",help_command=None ,intents=intents)

async def setup_plugins():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        plugins = config.get('autoload', [])
    except Exception as e :
        print(f'Error reading config : {e}')
        plugins = []
    
    for plugin in plugins:
        try:
            await bot.load_extension(f'plugins.{plugin}')
            print(f'Plugin loaded : {plugin}')
        except Exception as e :
            print(f'Loading error {plugin} : {e}')

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')

async def main():
    async with bot:
        await setup_plugins()
        with open('config.json', 'r') as f :
            config = json.load(f)
        token = config.get('token')
        if not token :
            print('Token invalide')
            return    
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())