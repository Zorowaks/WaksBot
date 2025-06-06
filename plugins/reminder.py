from discord.ext import commands
import discord
import datetime
import asyncio
import json
import os

reminder_file = "reminders.json"

class Reminder(commands.Cog):
    '''Gère les rappels.'''
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []
        self.load_reminders()

    def load_reminders(self):
        if os.path.exists(reminder_file):
            with open (reminder_file , 'r') as f:
                data = json.load(f)
                for r in data:
                    remind_time = datetime.datetime.fromisoformat(r["time"])
                    delay = (remind_time - datetime.datetime.now()).total_seconds()
                    if delay > 0 :
                        self.bot.loop.create_task(self.schedule_reminder(r['user_id'], r['task'], delay) )
        else:
            with open(reminder_file, 'w') as f:
                json.dump([], f)

    def save_reminder(self, user_id, task, remind_time):
        if os.path.exists(reminder_file):
            with open(reminder_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append({
            'user_id': user_id,
            'task': task,
            'time': remind_time.isoformat()
    })

        with open(reminder_file, 'w') as f:
            json.dump(data, f, indent=4)

    def delete_reminder(self, user_id, task):
        with open(reminder_file, 'r') as f:
            data =  json.load(f)
        
        data = [r for r in data if not (r['user_id'] == user_id and r['task'] == task) ]
        with open(reminder_file, 'w') as f:
            json.dump(data, f, indent=4)

    @commands.command(help='Permet de créer un rappel à une date précise.')
    async def remind(self, ctx, task: str, date: str, time:str):
        try:
            remind_time = datetime.datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
            now = datetime.datetime.now()
            delay = (remind_time - now).total_seconds()
            if delay <= 0:
                await ctx.send('Veuillez saisir un format de date valide')
                return
            
            self.save_reminder(ctx.author.id, task, remind_time)
            await self.schedule_reminder(ctx.author.id, task, delay)
            embed = discord.Embed(
                title='**Rappel ajouté**',
                description=f'Rappel ajouté par {ctx.author.mention} pour le {remind_time.strftime('%d/%m/%Y à %H:%M')} \n > Pseudo : {ctx.author} \n > Date : {remind_time.strftime('%d/%m/%Y %H:%M')}\n > Rappel : {task}',
                color=discord.Color(0x27C917)
            )
            embed.set_footer(text=f'{ctx.author.name}')
            await ctx.send(embed=embed)
        
        except ValueError:
            await ctx.send("Format invalide. Utilise `!remind \"tâche\" DD/MM/YYYY H:M`")

    async def schedule_reminder(self, user_id, task, delay):
        await asyncio.sleep(delay)
        user = self.bot.get_user(user_id)
        if user:
            try:
                embed = discord.Embed(
                    title='**Rappel :**',
                    description="N'oublie pas de faire {task}",
                    color=discord.Color(0xeee917)
                )
                await user.send(f'Rappel : **{task}**')
                self.delete_reminder(user_id, task)
            except:
                pass

    @commands.command(help='Permet de supprimer un rappel existant.')    
    async def cancelremind(self, ctx, task: str):
        user_id = ctx.author.id
        try:
            with open(reminder_file, 'r') as f :
                data = json.load(f)
        except FileNotFoundError:
            data = []

        before = len(data)
        data = [ r for r in data if not (r['user_id'] == user_id and r['task'].lower() == task.lower() )]
        after = len(data)

        with open(reminder_file, 'w') as f :
            json.dump(data, f, indent=4)

        if before == after :
            embed = discord.Embed(
                title='**Une erreur est survenue**',
                description=f'Aucun rappel nommé `{task}` trouvé',
                color=discord.Color.red()
            )
            embed.set_footer(text=f'{ctx.author.name}')
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(
                title='**Rappel supprimé**',
                description=f'`{task}` a bien été supprimé',
                color=discord.Color.orange()
            )
            embed.set_footer(text=f'{ctx.author.name}')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reminder(bot))