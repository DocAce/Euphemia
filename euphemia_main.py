import discord # pylint: disable=import-error
import tweepy # pylint: disable=import-error
import asyncio
import importlib
from types import ModuleType
import time
import euphemia
import euphemia_token

discordbot = discord.Client()
# twitterauth = tweepy.OAuthHandler(twitterapikey, twitterapisecretkey)
# twitterauth.set_access_token(twitteraccesstoken, twitteraccesstokensecret)
# twitterapi = tweepy.API(auth)
# https://docs.tweepy.org/en/latest/api.html

allow_reload = ['discord', 'tweepy', 'tracery', 'euphemia', 'euphemia_gens', 'euphemia_gm', 'dicey']
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

@discordbot.event
async def on_ready():
    print('Logged in as ' + discordbot.user.name + ' (ID: ' + str(discordbot.user.id) + ')')

@discordbot.event
async def on_message(message):
    if message.author != discordbot.user:
        isdm = message.guild is None
        if isdm and 'reload' in message.content: # only handle reload command in here, and only if it's a DM
            tmp = await message.channel.send('Reloading...')
            reload_modules(euphemia)
            await tmp.edit(content='Reload done.')
        else:
            await euphemia.handle_message(message, discordbot)

try:
    print('Running discord bot')
    discordbot.run(euphemia_token.token)
except Exception as e:
    print('Exception caught:')
    print(str(e))
