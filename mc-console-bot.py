import re
import threading
import discord
import subprocess
import os

from discord.ext import commands

### EDIT THIS BELOW ###

# Your bot's token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Minecraft server start script file path
MINECRAFT_SERVER_PATH = 'C:/path/to/start.sh'

# The role allowed to start the server
BOT_MASTER = 'ROLE_NAME'

### EDIT THIS ABOVE ###

if TOKEN == 'YOUR_DISCORD_BOT_TOKEN':
    print('No bot token! Replace \'YOUR_DISCORD_BOT_TOKEN\' with a valid Discord bot token in mc-server-bot.py!\nCheck README.md for info.')
    exit(0)

if not os.path.exists(MINECRAFT_SERVER_PATH):
    print('Could not find start script! Replace \'C:/path/to/start.sh\' with your server start script in mc-server-bot.py!\nCheck README.md for info.')
    exit(0)

# Discord bot client
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

server_process: subprocess.Popen

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.command()
async def startserver(ctx):
    
    global server_process
        
    bot_master = discord.utils.get(ctx.guild.roles, name=BOT_MASTER)
    
    if bot_master not in ctx.author.roles:
        await ctx.send('You don\'t have permission!')
        return
        
    if server_process.poll is None:
        await ctx.send('Server is already running!')
        return
    
    if not os.path.exists(MINECRAFT_SERVER_PATH):
        await ctx.send('Minecraft server start script not found.')
        return
        
    server_process = subprocess.Popen([MINECRAFT_SERVER_PATH], cwd=os.path.dirname(MINECRAFT_SERVER_PATH),
                                      stdout=subprocess.PIPE,
                                      stdin=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      universal_newlines=True)
    await ctx.send('Starting Minecraft server...')
    
    while True:
        line = server_process.stdout.readline()
        if not line:
            continue
        
        line = line.strip()
        print(line)  # Optional: Print server output to console
    
        if re.search(r'\d{2}:\d{2}:\d{2} INFO]: Done \(\d+\.\d+s\)', line):
            await ctx.send('Minecraft server is up and running!')
            break
                 
    global input_thread
       
    input_thread = threading.Thread(target = wait_user_input, args=[server_process])
    output_thread = threading.Thread(target = wait_console_output, args=[server_process])
    
    input_thread.start()
    output_thread.start()
    
def wait_user_input(server_process: subprocess.Popen):
    
        while server_process.poll() is None:
            try:
                i = input()
                print('Input: ' + i)
                server_process.stdin.write(i + "\n")
                server_process.stdin.flush()
                
            except KeyboardInterrupt:
                print('Stopping Minecraft server...')
                server_process.stdin.write('stop\n')
                return
                            
def wait_console_output(server_process):
    global input_thread
    try:
        while server_process.poll() is None:
            o = server_process.stdout.readline()
            print(o.strip())
            
        
    except KeyboardInterrupt:
        input_thread.join
        return

bot.run(TOKEN)
