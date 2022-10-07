import discord # pylint: disable=import-error
import os
import random
import json
import euphemia_gens

gamedatafilename = 'game.json'
gamedata = {}

if os.path.isfile(gamedatafilename):
    print('Trying to open file ' + gamedatafilename + ' for loading')
    with open(gamedatafilename) as gamedatafile:
        if os.stat(gamedatafilename).st_size > 0:
            print('Loading game file ' + gamedatafilename)
            gamedata = json.load(gamedatafile)
        else:
            print('Game file is empty')
else:
    print('Game file does not exist')

def save_game_data():
    print('Trying to open file ' + gamedatafilename + ' for saving')
    with open(gamedatafilename, 'w') as gamedatafile:
        print('Saving ' + gamedatafilename)
        json.dump(gamedata, gamedatafile)

def generate_character():
    race = random.choice(euphemia_gens.player_races)
    gender = random.choice(["male", "female"])
    return {
        "race": race,
        "gender": gender,
        "name": euphemia_gens.generate_x_name(race, gender)
    }

def reroll_character_race(user):
    gamedata[user.id]["race"] = random.choice(euphemia_gens.player_races)
    reroll_character_name(user)

def reroll_character_gender(user):
    gamedata[user.id]["gender"] = random.choice(["male", "female"])
    reroll_character_name(user)

def reroll_character_name(user):
    character = gamedata[user.id]
    character["name"] = euphemia_gens.generate_x_name(character["race"], character["gender"])

def reroll_character(user):
    gamedata[user.id] = generate_character()

def print_character(user):
    character = gamedata[user.id]
    print(str(character))
    print(str(gamedata[user.id]))
    return character["name"] + ', a ' + character["gender"] + ' ' + character["race"]

def handle_message(message, commands, args):
    if not message.author.id in gamedata:
        reroll_character(message.author)
    msgstring = ''
    if 'reroll' in commands:
        if 'name' in commands:
            reroll_character_name(message.author)
        elif 'gender' in commands:
            reroll_character_gender(message.author)
        elif 'race' in commands:
            reroll_character_race(message.author)
        else:
            reroll_character(message.author)
        msgstring = 'Reroll done. Your character is now ' + print_character(message.author)
    elif 'info' in commands:
        msgstring = 'Your character is ' + print_character(message.author)
    save_game_data()
    return msgstring
