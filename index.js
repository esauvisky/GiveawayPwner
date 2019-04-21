// jshint esversion: 6
/*
Author: Emi Bemol <esauvisky@gmail.com>
*/

// Libraries
const Discord = require('discord.js');
const colors = require('colors');
const fs = require("fs");
var spawn = require('child_process').spawn;
var theList = [];

// Grabs configs from the JSON file
hotload = require("hotload");
var first_time = true;
config = hotload('./config.json.js', function(config2) {
    if (! first_time) {
        spawn('notify-send', ['GiveawayPwner', 'Reloading configs...']);
    } else {
        first_time = false;
    }
});

spawn('notify-send', ['GiveawayPwner', 'DO NOT FORGET TO PARTICIPATE']);

// Here we define our client, most people call it "client" but I prefer to call it "bot".
bot = new Discord.Client({forceFetchUsers: true});

// When our bot is ready.
bot.on("ready", () =>{
    // We will send a message to our console telling us that the bot has initiated correctly.
    console.log('The bot is online!'.green);
    console.log('Your username is: '.green.bold + bot.user.tag.bold);
    console.log('Do not forget to participate!!'.yellow.bold);
});

// When a message is received, run the following code.
bot.on("message", (message) => {
    let channelId = String(message.channel).substring(2, String(message.channel).length - 1);

    // Bails out if not #giveaway channel
    if (channelId != '480597151383158795') { return; }

    // Debug (chatroom channel)
    // if (channelId != '260979786145333248') { return; }


    // let msg = String(message.content).replace(/\n/g, ' ').trim()
    let msg = String(message.content).replace(/\n/g, ' ').trim().toLowerCase();


    // Only adds the number to the array if it's unique (i.e.: the first time it's being submitted)
    if (theList.indexOf(msg) === -1) {
        theList.push(msg);
        fs.appendFile('messages.log', msg + '\n', function (err) {});
        console.log('\nUnique Answer: ' + msg.blue.bold + ' (by ' + message.author.tag + ')');
    } else {
        process.stdout.write("-");
    }
});

/**********************************
********** Weird Stuff! ***********
**********************************/
// Suppreses Undhandled Promise Rejections
bot.on("unhandledRejection", (reason, p) => {
    if (config.debugMode) {
        console.log(colors.red.bold("Discord's unhandled Rejection:"));
        console.log(colors.red("- Reason:\t" + `${reason}`));
        console.log(colors.red("- Promise:\t" + `${require("util").inspect(p, {depth: 3})}`));
    }
});
// This tests the suppresion below
//new Promise((_, reject) => reject({ test: 'woops!' }));

// Logs warnings and errors
bot.on("warning", (warning) => {
    console.log(colors.red.bold("A warning ocurred!"));
    console.log(colors.red(warning.name));
    console.log(colors.red(warning.message));
    console.log(colors.red(warning.stack));
});
bot.on("error", (error) => {
    console.log(colors.red.bold("An error ocurred!"));
    console.log(colors.red(error.name));
    console.log(colors.red(error.message));
    console.log(colors.red(error.stack));
});
bot.login(config.token); // Login as our bot using the token specified in config.json.
