import discord
import asyncio
import json
import tracery
from tracery.modifiers import base_english
from random import randint

client = discord.Client()

with open('xnames.json') as xnamesfile:
    xnames = tracery.Grammar(json.load(xnamesfile))
    xnames.add_modifiers(base_english)

help_text = 'Valid commands:\n!roll: rolls a number of dice and adds the results together. Example: !roll 3d12+7\n!flip: flips a number of coins. Example: !flip 3\n!help: you already know what it does!'

def roll_die(sides):
    return randint(1, sides)

def flip_coin():
    if randint(0, 1) == 0:
        return 'Heads'
    else:
        return 'Tails'
    
def generate_coin_flip_output(params):
    if params == '':
        numflips = 1
    else:
        numflips = int(params)
    result = ''
    for i in range(numflips):
        if i > 0:
            result += ', '
        result += flip_coin()
    return result

def generate_dice_roll_output(params):
    numdice = 1
    index_d = params.find('d')
    if index_d > 0:
        numdice = int(params[:index_d])
        params = params[index_d + 1:]
    elif index_d == 0:
        params = params[1:]
    index_operator = params.find('+')
    addsgn = 1
    if index_operator == -1:
        index_operator = params.find('-')
        addsgn = -1
    add = 0
    if index_operator != -1:
        add = int(params[index_operator + 1:]) * addsgn
        params = params[:index_operator]
    sides = 6
    if params != '':
        sides = int(params)
    total = add
    result = 'Rolling ' + str(numdice) + 'd' + str(sides)
    if add < 0:
        result += '-'
    else:
        result += '+'
    result += str(abs(add)) + '\n'
    result += 'Rolls: '
    for i in range(numdice):
        rollresult = roll_die(sides)
        total += rollresult
        if i > 0:
            result += ', '
        result += str(rollresult)
    result += '\nTotal: ' + str(total)
    return result

def isracename(string):
    lowercase = string.lower()
    return lowercase == 'argon' or lowercase == 'boron' or lowercase == 'paranid' or lowercase == 'split' or lowercase == 'teladi' or lowercase == 'terran'

def isgender(string):
    lowercase = string.lower()
    return lowercase == 'male' or lowercase == 'female'

def generate_name(params):
    race = ''
    gender = ''
    args = params.split(' ')
    for arg in args:
        if isgender(arg):
            gender = arg
        elif isracename(arg):
            race = arg
    origin = '#name#'
    if race != '' or gender != '':
        origin = '#' + race + gender + '#'
    return xnames.flatten(origin)

def generate_character(params):
    return xnames.flatten("#origin#")

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID: ' + client.user.id + ')')

@client.event
async def on_message(message):
    params = message.content.strip()
    if params.startswith('!help'):
        await client.send_message(message.channel, help_text)
    elif params.startswith('!flip'):
        await client.send_message(message.channel, generate_coin_flip_output(params[6:]))
    elif params.startswith('!roll'):
        await client.send_message(message.channel, generate_dice_roll_output(params[6:]))
    elif params.startswith('!name'):
        await client.send_message(message.channel, generate_name(params[6:]))
    elif params.startswith('!char'):
        await client.send_message(message.channel, generate_character(params[6:]))
"""
    elif message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping.')
    elif message.content.startswith('!tracery'):
        await client.send_message(message.channel, grammar.flatten('#origin#'))
"""

client.run('NDkzNDU4MDUzNjE4NzI4OTYw.DpqD0w.chBsknZdatizKNVGUd2F8P5lvHI')
