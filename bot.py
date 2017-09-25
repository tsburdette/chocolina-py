import discord
from discord.ext import commands
import asyncio
import re
import json
import logging
from pybooru import Danbooru
import urllib.request

initial_extensions = [ 'butts', 'danbooru' ]

with open('config.json') as config_file:
    config = json.load(config_file)
discord_token = config['discord_token']
bot = commands.Bot(command_prefix=config['command_prefix'], description=config['description'])

log = logging.getLogger(__name__)

@bot.command()
async def load(extension_name : str):
    """Loads an extension"""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

@bot.event
async def on_message(message):
    print('[{0}] {1} : {2}'.format(message.channel, message.author, message.content))
    if message.author == bot.user:
        return
    if re.match(r'who$|who[!?\n\r]+', message.content, re.IGNORECASE):
        print('Found match')
        await bot.send_file(message.channel, 'images/chocobocolina.gif')
    await bot.process_commands(message)

@bot.group(pass_context=True)
async def role(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('I am fulfilling my role as best I can! :D')

@role.command()
async def list(member : discord.Member):
    role_list = ', '.join(role.name for role in member.roles[1:])
    await bot.say('{0.name}\'s roles are {1}.'.format(member, role_list))

@role.command(pass_context = True)
async def add(ctx, *, role : str):
    safe_roles = [
        "battle bunnies",
        "camp counselors",
        "potluckers",
        "puhbuhguh when",
        "ksr soldiers"
        ]
    server_role_list = ctx.message.server.roles[1:]
    server_role_names = [role.name.lower() for role in server_role_list]
    mapping = dict(zip(server_role_names, server_role_list))
    print(role.lower())
    await bot.say('Attempting to add {0} to role: {1}'.format(ctx.message.author, role))
    if role.lower() in safe_roles:
        if role.lower() in server_role_names:
            try:
                await bot.add_roles(ctx.message.author, mapping[role.lower()])
                await bot.say('Added {0} to role: {1}'.format(ctx.message.author, role))
            except:
                await bot.say('Something went wrong! D:')
        else:
            await bot.say('That role doesn\'t exist!')
    else:
        await bot.say('That role is beyond my simple powers. Sorry!')

@role.command(pass_context = True)
async def remove(ctx, *, role : str):
    safe_roles = [
        "battle bunnies",
        "camp counselors",
        "potluckers",
        "puhbuhguh when",
        "ksr soldiers"
        ]
    user_role_list = ctx.message.author.roles[1:]
    user_role_names = [role.name.lower() for role in user_role_list]
    mapping = dict(zip(user_role_names, user_role_list))
    await bot.say('Attempting to remove {0} from role: {1}'.format(ctx.message.author, role))
    if role.lower() in safe_roles:
        if role.lower() in user_role_names:
            try:
                await bot.remove_roles(ctx.message.author, mapping[role.lower()])
                await bot.say('Removed {0} from role: {1}'.format(ctx.message.author, role))
            except:
                await bot.say('Something went wrong! D:')
        else:
            await bot.say('You don\'t have that role!')
    else:
        await bot.say('That role is beyond my simple powers. Sorry!')


if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{} : {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(discord_token)
