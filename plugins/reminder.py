from discord.ext import commands
from discord import app_commands
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

    def get_next_reminder_id(self):
        if os.path.exists(reminder_file):
            with open(reminder_file, 'r') as f :
                try:
                    data = json.load(f)
                    ids = [r.get("id", 0) for r in data]
                    return max(ids, default=0) + 1
                except json.JSONDecodeError :
                    return 1
        return 1          
    
    def load_reminders(self):
        if os.path.exists(reminder_file):
            with open (reminder_file , 'r') as f:
                data = json.load(f)
                for r in data:
                    remind_time = datetime.datetime.fromisoformat(r["time"])
                    delay = (remind_time - datetime.datetime.now()).total_seconds()
                    if delay > 0 :
                        self.bot.loop.create_task(self.schedule_reminder(r['user_id'], r['task'], delay, r['id']) )
        else:
            with open(reminder_file, 'w') as f:
                json.dump([], f)

    def save_reminder(self, user_id, task, remind_time):
        reminder_id = self.get_next_reminder_id()

        if os.path.exists(reminder_file):
            with open(reminder_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append({
            'id' : reminder_id,
            'user_id': user_id,
            'task': task,
            'time': remind_time.isoformat()
        })

        with open(reminder_file, 'w') as f:
            json.dump(data, f, indent=4)

        return reminder_id    

    def delete_reminder(self, user_id, reminder_id):
        with open(reminder_file, 'r') as f:
            data =  json.load(f)
        
        data = [r for r in data if not (r['user_id'] == user_id and r['id'] == reminder_id) ]
        with open(reminder_file, 'w') as f:
            json.dump(data, f, indent=4)

    @app_commands.command(name="remind", description="Créer un rappel")
    @app_commands.describe(task='Tâche à rappeler', date='JJ/MM/AAAA', time='HH:MM')
    async def remind(self, interaction: discord.Interaction ,task: str, date: str, time:str):
        try:
            remind_time = datetime.datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
            now = datetime.datetime.now()
            delay = (remind_time - now).total_seconds()
            if delay <= 0:
                await interaction.response.send_message('Veuillez saisir un format de date valide')
                return
            
            reminder_id = self.save_reminder(interaction.user.id, task, remind_time)
            self.bot.loop.create_task(self.schedule_reminder(interaction.user.id, task, delay, reminder_id))
            embed = discord.Embed(
                title='Rappel ajouté',
                description=f'Rappel ajouté par {interaction.user.mention} pour le {remind_time.strftime('%d/%m/%Y à %H:%M')} \n > Pseudo : {interaction.user.name} \n > Date : {remind_time.strftime('%d/%m/%Y %H:%M')}\n > Rappel : {task}',
                color=discord.Color(0x27C917)
            )
            embed.set_footer(text=f'ID : {reminder_id}')
            await interaction.response.send_message(embed=embed)
        
        except ValueError:
            await interaction.response.send_message("Format invalide. Utilise `!remind \"tâche\" DD/MM/YYYY H:M`")

    async def schedule_reminder(self, user_id, task, delay, reminder_id):
        await asyncio.sleep(delay)
        user = self.bot.get_user(user_id)
        if user:
            try:
                embed = discord.Embed(
                    title='**Rappel :**',
                    description=f"N'oublie pas de faire {task}",
                    color=discord.Color(0xeee917)
                )
                await user.send(embed=embed)
                self.delete_reminder(user_id, reminder_id)
            except:
                pass

    @app_commands.command(name="cancelremind", description="Supprime un rappel")
    @app_commands.describe(reminder_id="ID du rappel à supprimer")   
    async def cancelremind(self, interaction: discord.Interaction, reminder_id : int):
        user_id = interaction.user.id
        with open(reminder_file, 'r') as f :
            data = json.load(f)

        if any(r['user_id'] == user_id and r['id'] == reminder_id for r in data):
            self.delete_reminder(user_id, reminder_id)
            embed=discord.Embed(
                title='**Rappel supprimé**',
                description=f"Le rappel avec l'ID `{reminder_id}` a bien été supprimé",
                color=discord.Color.orange()
            )
            embed.set_footer(text=f'{interaction.user}')
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
            title='**Une erreur est survenue**',
            description=f"Aucun rappel avec l'ID `{reminder_id}` trouvé",
            color=discord.Color.red()
            )
            embed.set_footer(text=f'{interaction.user.name}')
            await interaction.response.send_message(embed=embed)


    @app_commands.command(name="remindlist", description="Voir la liste de ses rappels")
    @app_commands.describe()
    async def remindlist(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        with open(reminder_file, 'r') as f :
            data = json.load(f)
        
        user_reminders = [r for r in data if r['user_id'] ==  user_id]

        if not user_reminders:
            await interaction.response.send_message("Vous n'avez aucun rappel.")
            return
        
        embed = discord.Embed(
            title='**Vos rappels** :',
            color=discord.Color(0x1d4ea6)
        )

        for r in user_reminders:
            remind_time = datetime.datetime.fromisoformat(r['time'])
            embed.add_field(
                name=f"ID : {r['id']}",
                value=f"**Date** : {remind_time.strftime('%d/%m/%Y %H:%M')}\n **Tâche** : {r['task']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Reminder(bot))