var kill = require('tree-kill');
var spawn = require('child_process').spawn;
var discord = require("discord.js");

var bot = new discord.Client({ intents: ["GUILDS", "GUILD_MESSAGES"] });
var mcserver;

// CHANGE THE VARIABLES BELOW
// CHECK README.MD FOR DIRECTIONS

// The path to 'start.bat'
var MC_SERVER_START_SCRIPT = "C:/Users/username/start.bat";

// The channel ID of your game chat channel
var gamechat = "<ID_HERE_WITHOUT_BRACKETS>"

// The name of the role allowed to start, kill, and send commands to the server
var consolemaster = "<NAME_HERE_WITHOUT_BRACKETS>"

// ONE MORE EDIT AT THE BOTTOM OF THE SCRIPT
// CHECK README.MD FOR DIRECTIONS

bot.on("ready", () => {
    console.log('Bot online! Woohoo!');
    bot.user.setActivity('the Minecraft Server', { type: 'WATCHING' })
});

bot.on("messageCreate", function (message) {

    // If message is "start" by consolemaster
    if (message.content == "start" && message.member.roles.cache.some(role => role.name === consolemaster)) {

        console.log('Attempting to start server.');
        // Only start if not running
        if (mcserver == null) {

            message.channel.send("**Starting Minecraft server. This will take a minute or so.**");

            // Start the server
            mcserver = spawn(MC_SERVER_START_SCRIPT);

            // Server log -> script log
            mcserver.stdout.on('data', function (data) {
                console.log("" + data);

                // Server log -> Discord
                if (data.length < 2001) {
                    message.channel.send("" + data);
                } else if (data.length > 2000) {
                    message.channel.send("**This message was too long to send! " + data.length + " > 2000! Here's the cut version:**");
                    message.channel.send("" + data.slice(0, 2000));
                }

                // Look for chat message
                if (data.slice(10, 18) == "INFO]: <") {

                    // Send message to Discord
                    bot.channels.cache.get(gamechat).send(data.toString().split("INFO]: ")[1]);
                }
            });

            mcserver.on('close', function (code) {
                console.log("child process exited with code " + code);
                message.channel.send("Minecraft server has been closed. (Code: " + code + ")");

                message.guild.channels.resolve(serverstatus).setName('SERVER: DOWN ❌');

                // Stop the server
                if (mcserver != null) {
                    kill(mcserver.pid);

                }


                mcserver = null;
            });
        }
        else {
            message.channel.send("**Minecraft server is already running.**");
        }

    } else if (message.content == "kill" && message.member.roles.cache.some(role => role.name === consolemaster)) {

        // Only stop if running
        if (mcserver != null) {
            message.channel.send("**Force-stopping Minecraft server...**");

            // Stop the server
            kill(mcserver.pid);
            mcserver = null;
        }
        mcserver = null;

    } else if (message.content.startsWith("-") && message.member.roles.cache.some(role => role.name === consolemaster) && (mcserver != null)) {
        var command = message.content.slice(1)
        mcserver.stdin.write(command + '\n');

        // in-game discord -> Minecraft
    } else if (message.channel.id == gamechat && mcserver != null && message.author.id != bot.user.id) {

        mcserver.stdin.write('tellraw @a [{\"text\":\"[Discord]\",\"color\":\"gray\"}, {\"text\":\" ' + message.author.username + ': \",\"color\":\"dark_aqua\"},{\"text\":\"' + message.content + '\",\"color\":\"white\"}]' + '\n');    

        

    }

});


// Put your bot token below
bot.login("<BOT_TOKEN_WITHOUT_BRACKETS>");
