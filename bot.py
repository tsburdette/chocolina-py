import discord
from discord.ext import commands
import asyncio
import re
import json
import logging
from pybooru import Danbooru
import urllib.request

with open('config.json') as config_file:
    config = json.load(config_file)
discord_token = config['discord_token']
bot = commands.Bot(command_prefix=config['command_prefix'], description=config['description'])
danbooru_client = Danbooru('danbooru')

log = logging.getLogger(__name__)

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

@bot.command()
async def butts():
    await bot.say('Butts are great!')

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
        "camp counselors"
        ]
    server_role_list = ctx.message.server.roles[1:]
    server_role_names = [role.name.lower() for role in server_role_list]
    mapping = dict(zip(server_role_names, server_role_list))
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
        "camp counselors"
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

@bot.command()
async def react(*tags : str):
    if len(tags)==0:
        tags = ('trap',)
    print('Seeking image for ' + ' '.join(tags))
    try:
        posts = danbooru_client.post_list(tags=' '.join(tags), random=True, limit=1)
        url = 'https://danbooru.donmai.us' + posts[0]['file_url']
        await bot.say(url)
    except:
        await bot.say('Sorry. I couldn\'t find any images using these tags: ' + ' '.join(tags))

bot.run(discord_token)
