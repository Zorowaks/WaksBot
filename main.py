# WaksBot
# Copyright (c) 2025 Carol Legout-Sales
# Licensed under the MIT License. See the LICENSE file for details.

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions
import json
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("Token")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!",help_command=None ,intents=intents)
tree = bot.tree

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
    await bot.wait_until_ready()
    try:
        await bot.tree.sync()
        print('Synchronized slash commands')
    except Exception as e :
        print(f'Synchronization error : {e}')
    print(f'Logged on as {bot.user}')

async def main():
    async with bot:
        await setup_plugins()
        with open('config.json', 'r') as f :
            config = json.load(f)
            if not token :
                raise ValueError('Token manquant')
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())