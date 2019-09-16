import discord # pylint: disable=import-error
import asyncio
import importlib
from types import ModuleType
import time
import euphemia

bot = discord.Client()

allow_reload = ['discord', 'tracery', 'euphemia', 'euphemia_gens', 'euphemia_gm', 'dicey']
modules_to_reload = []

def get_modules_recursive(module):
    print('Reloading ' + str(module))
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if type(attribute) is ModuleType and not attribute in modules_to_reload and attribute_name in allow_reload:
            get_modules_recursive(attribute)
    modules_to_reload.append(module)

def reload_modules(basemodule):
    modules_to_reload.clear()
    get_modules_recursive(basemodule)
    for module in modules_to_reload:
        importlib.reload(module)

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (ID: ' + bot.user.id + ')')

@bot.event
async def on_message(message):
    if message.author != bot.user:
        isdm = message.server is None
        if isdm and 'reload' in message.content: # only handle reload command in here, and only if it's a DM
            tmp = await bot.send_message(message.channel, 'Reloading...')
            reload_modules(euphemia)
            await bot.edit_message(tmp, 'Reload done.')
        else:
            await euphemia.handle_message(message, bot)

while True:
    try:
        print('Running bot')
        bot.run('')
    except Exception as e:
        print('Exception caught:')
        print(str(e))
        print('Rerunning in 5 seconds')
        time.sleep(5)
