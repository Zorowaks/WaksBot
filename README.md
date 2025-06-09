# WaksBot

WaksBot is a custom Discord bot designed to assist servers with management features, ModMail, modular plugins, and much more.  
Easy to configure, scalable and designed to manage your discord servers.

## Main features

- **Admin** : Bot management
- **Help** : A more terse help command.
- **Manager** : Plugin management
- **Reminder**: Recall programming system
- **ModMail**: A private messaging system between users and staff through DMs.
- **Modular configuration**: Plugins are dynamically loaded via `config.json`.

## Commands 

**Admin** :

- `shutdown` -> turn off bot.
- `restart` -> restart the bot.
- `sync` -> synchronizes commands.

**Help** :

 - `help` -> Display the list of available commands.
 - `help <command>` -> displays information about the command

**Manager** :

  - `load <plugin>` -> Load a plugin.
  - `reload <plugin>` ->  Reload a plugin.
  - `unload <plugin>` -> Unload a plugin.

**Reminder** : 

  - `remind <task> <DD/MM/YYYY> <HH:MM>` -> Set a reminder.
  - `remindlist` -> See the list of reminders.
  - `cancelremind <id>` -> Remove a reminder.

**ModMail** :

  - `setmodmail <#channel>` ->  Set a channel where ModMail messages arrive.
  - `modmail <server> <message>` -> Sends a modmail (for MP use only)
  - `reply <user> <message>` -> Reply to a user’s direct message.
  
## Installation

1. **Clone the project** :
   ```bash
   git clone https://github.com/Zorowaks/WaksBot.git

2. **Install dependencies** :
    ```bash
    pip install -r requirements.txt

3. **Configure the environment** :

    Creates an `.env` file:
   ```env
   Token=YOUR_TOKEN_DISCORD

4. **Add your plugins to `config.json`** :

   The plugin manager is mandatory at startup, otherwise you won't be able to add other plugins afterwards.
    ```json
    {
    "autoload" : ["manager", "help", "modmailconfig"]
    }
6. **Launch the bot** :
     ```bash
     py main.py

## License

This project is licensed under the MIT License.  
You are free to use, modify, and redistribute it, as long as you include the original license notice.  
[Learn more about the MIT License](https://opensource.org/licenses/MIT)

##  Author

Developed by [@Zorowaks](https://github.com/Zorowaks) — feel free to open an issue or submit a pull request!  
You can also contact me directly on Discord: `zorowaks_`
