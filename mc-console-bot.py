import asyncio
import re
import threading
import discord
import subprocess
import os

from discord.ext import commands

#==-----------------------------------------==#
# EDIT THE VALUES BELOW                       #
# See README.md for more information          #
#                                             #
# Your bot's token                            #
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'              #
#                                             #
# Minecraft server start script file path     #
MINECRAFT_SERVER_PATH = 'C:/path/to/start.sh' #
#                                             #
# The role allowed to start the server        #
BOT_MASTER = 'ROLE_NAME'                      #
#                                             #
#==-----------------------------------------==#

# Below is the script. Do not edit this unless you know what you're doing!

SERVER_START_COMMAND = [MINECRAFT_SERVER_PATH]

# Init Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Init server process and status
server_process = None
server_running = False

# Prevent concurrent access to server_process
server_lock = threading.Lock()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")

@bot.command()
async def startserver(ctx):
    global server_process, server_running

    # Check if the user has the 'BOT_MASTER_ROLE_NAME' role
    bot_master_role = discord.utils.get(ctx.guild.roles, name=BOT_MASTER)
    if bot_master_role not in ctx.author.roles:
        await ctx.send("You don't have permission to start the server.")
        return

    # Check if the server is already running
    if server_running:
        await ctx.send("The server is already running.")
        return

    # Check if the server start script exists
    if not os.path.exists(MINECRAFT_SERVER_PATH):
        await ctx.send("Minecraft server start script not found.")
        return

    # Start the server asynchronously
    await ctx.send("Starting Minecraft server...")
    try:
        with server_lock:
            server_process = await asyncio.create_subprocess_exec(
                *SERVER_START_COMMAND,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(MINECRAFT_SERVER_PATH),
                universal_newlines=False,
            )

        # Set server_running flag
        server_running = True

        # Print server output to the console
        while server_running:
            stdout_line = await server_process.stdout.readline()
            if not stdout_line:
                break
            stdout_line = stdout_line.decode("utf-8").strip()
            print(stdout_line)

            # Check if the line matches the server startup completion pattern
            if re.search(r'\[\d{2}:\d{2}:\d{2} INFO\]: Done \(\d+\.\d+s\)!', stdout_line):
                await ctx.send("Minecraft server is up and running!")

        await ctx.send("Minecraft server has stopped.")
        server_running = False
    except Exception as e:
        await ctx.send(f"An error occurred while starting the server: {e}")

# Function to read console commands from the terminal
def read_console_input():
    global server_process, server_running
    while True:
        try:
            if server_running:
                command = input()
                with server_lock:
                    server_process.stdin.write((command + "\n").encode('utf-8'))
                    
        except KeyboardInterrupt:
            # Stop the server
            print("Stopping Minecraft server...")
            server_process.terminate()
            try:
                asyncio.wait_for(server_process.wait(), timeout=30)
            except asyncio.TimeoutError:
                print("Server did not stop gracefully. Forcefully terminating.")
                server_process.kill()

if __name__ == "__main__":
    # Start a thread to read console input
    console_input_thread = threading.Thread(target=read_console_input)
    console_input_thread.daemon = True
    console_input_thread.start()
    
    bot.run(TOKEN)