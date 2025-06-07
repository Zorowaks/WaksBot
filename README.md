# WaksBot

WaksBot is a custom Discord bot designed to assist servers with management features, ModMail, modular plugins, and much more.  
Easy to configure, scalable and designed to manage your discord servers.

## Main features

- **ModMail**: A private messaging system between users and staff through DMs.
- **Modular configuration**: Plugins are dynamically loaded via `config.json`.
- **Custom commands**:
  - `!setmodmail` — Sets the channel where ModMail messages will be sent.
  - `!reply` — Allows staff to respond to users' direct messages.

## Installation

1. **Clone the project** :
   ```bash
   git clone https://github.com/Zorowaks/WaksBot.git
   cd WaksBot

2. **Install dependencies** :
    ```bash
    pip install -r requirements.txt

3. **Configure the environment** :

    Creates an `.env` file:
   ```env
   Token=YOUR_TOKEN_DISCORD

4. **Add your plugins to `config.json`** :
    ```json
    {
    "autoload" : ["manager", "help", "modmailconfig"]
    }
5. **Launch the bot** :
     ```bash
     py main.py

## License

This project is licensed under the MIT License.  
You are free to use, modify, and redistribute it, as long as you include the original license notice.  
[Learn more about the MIT License](https://opensource.org/licenses/MIT)

##  Author

Developed by [@Zorowaks](https://github.com/Zorowaks) — feel free to open an issue or submit a pull request!  
You can also contact me directly on Discord: `zorowaks_`
