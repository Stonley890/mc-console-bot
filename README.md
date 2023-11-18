# mc-console-bot
A Python script that lets you start your Minecraft server using a Discord bot.

## Installation
### 1. Download the file
Download the [script](mc-console-bot.py) from the repository.

### 2. Prepare Discord
Create a role that you want to allow access to console commands.

### 3. Create a bot
1. Go to https://discord.com/developers/applications and create a new application. Give it any name, description, or icon.
2. Go to the **Bot** tab and create a bot. Give it a name.
3. Under the **OAuth2** tab, go to **URL Generator**. Check the _bot_ box. In the second table, check the _Read Messages/View Channels_ box.
4. Scroll down and look for MESSAGE CONTENT INTENT under _Privileged Gateway Intents_. Enable the toggle.
5. Copy the URL and open it. Invite the bot to your server. Go back to the **Bot** tab and find the _Bot Token_. Reset and copy it. We'll need it later.

### 4. Edit the script
1. Open the script using a text editor.
2. Find `TOKEN`. Replace `YOUR_DISCORD_BOT_TOKEN` with the bot token you copied earlier.
3. Find `MINECRAFT_SERVER_PATH`. Replace `C:/path/to/start.sh` with the full path to your start.bat, start.sh, or start.command file.
   - _If you don't have a start command file, you can generate one at http://flags.sh/._
4. Find `CONSOLE_MASTER`. Replace `ROLE_NAME` with the name of the role you want to allow to start the server.

### 5. Download and Install Python
1. If you already have Python installed, skip to step six.
2. Go to https://www.python.org/downloads/ and either download the latest source release or (if using Linux) install `python3` using your package manager.
3. Follow the installation steps.

### 6. Install required packages
1. Open the terminal or Windows Powershell and execute the following command.
```bash
python3 -m pip install -U discord.py
```

**You're done with the installation!**

## Operation
Let's go through the process of using the bot.

1. Using the terminal or Windows Powershell, run `python3 path/to/mc-console-bot.py`, replacing **path/to/mc-console-bot.py** with the path to the script.
2. If you see `Logged in as (bot username) - (bot client ID)` the bot has successfully connected.
3. In your Discord server, use `$startserver` to start the server. Make sure you have the console master role.

That's it!

### Security
**Q:** Is this safe?
**A:** Yes. This script does not make any outside connections other than Discord.

**Q:** How do I know only my bot can access the script?
**A:** Your bot ID links ONLY to your bot. Even if someone manages to get your bot token (which you should NEVER share with anyone), they will only be able to control the bot, not the server.

### Troubleshooting
#### **The script throws errors when I run it.**
Make sure you have a valid bot token.
#### **What is a start script?**
A start script is a script that runs your Minecraft server JAR file. You can generate one at http://flags.sh/.
#### **I have a valid start script, but the bot throws errors when I run $startserver**
Make sure the path to your start script is formatted correctly. If the bot script and the start script are in the same folder, you can set `MINECRAFT_SERVER_PATH` to `./start.sh` (or whatever your script is called.)

If you set a definite path make sure you prepend spaces with a backslash (\\): `/home/stonley890/Desktop/Minecraft\ Server/start.sh`. In this case, the `Minecraft Server` folder needs a \\ before the space.

If it still doesn't work, you may need to specify how to run the script. If your start script ends in `.sh`, add a new line to the top of it:
```sh
#!/bin/bash
```

#### **The bot says `[Errno 13] Permission denied`**
Try relocating the `mc-console-bot.py` script inside your server folder and setting the variable locally.
```python
MINECRAFT_SERVER_PATH = './start.sh'
```
For more info, see https://github.com/Stonley890/mc-console-bot/issues/7.
