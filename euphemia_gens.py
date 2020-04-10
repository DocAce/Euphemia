import json
import tracery # pylint: disable=import-error
from tracery.modifiers import base_english # pylint: disable=import-error
import markovify # pylint: disable=import-error
import string

with open('xnames.json') as xnamesfile:
    print('Loading xnames.json')
    xnames = tracery.Grammar(json.load(xnamesfile))
    xnames.add_modifiers(base_english)

with open('dungeonworld.json') as dungeonworldfile:
    print('Loading dungeonworld.json')
    dungeonworld = tracery.Grammar(json.load(dungeonworldfile))
    dungeonworld.add_modifiers(base_english)

with open('dwpw.json') as dwpwfile:
    print('Loading dwpw.json')
    dwpw = tracery.Grammar(json.load(dwpwfile))
    dwpw.add_modifiers(base_english)

with open('gmprompt.json') as gmpromptfile:
    print('Loading gmprompt.json')
    gmprompt = tracery.Grammar(json.load(gmpromptfile))
    gmprompt.add_modifiers(base_english)

with open('eldergod.json') as eldergodfile:
    print('Loading eldergod.json')
    eldergod = tracery.Grammar(json.load(eldergodfile))
    eldergod.add_modifiers(base_english)

with open('xpatch.txt') as xpatchfile:
    print('Loading xpatch.txt')
    xpatchtext = xpatchfile.read()
    xpatchmodel = markovify.NewlineText(xpatchtext)
    print('xpatch.txt loaded and processed')

races = ['argon', 'boron', 'paranid', 'split', 'teladi', 'terran', 'xenon']
player_races = ['argon', 'boron', 'paranid', 'split', 'teladi', 'terran']
genders = ['male', 'female', 'lar']

def isracename(string):
    return string.lower() in races

def isgender(string):
    return string.lower() in genders

def is_race_gendered(string):
    return string.lower() != 'xenon'

def get_race_from_args(args):
    for arg in args:
        if isracename(arg):
            return arg
    return ''

def get_gender_from_args(args):
    for arg in args:
        if isgender(arg):
            return arg
    return ''

def generate_x_name(race, gender):
    origin = '#name#'
    if race != '' or gender != '':
        if race != '' and not is_race_gendered(race):
            gender = ''
        origin = '#' + race + gender + '#'
    print('generate_x_name uses origin ' + origin)
    return xnames.flatten(origin)

def generate_x_name_from_args(args):
    return generate_x_name(get_race_from_args(args), get_gender_from_args(args))

def generate_x_sector(race):
    if race != '':
        origin = '#' + race + 'sector#'
    else:
        origin = '#sector#'
    print('generate_x_name uses origin ' + origin)
    return xnames.flatten(origin)

def generate_x_sector_from_args(args):
    return generate_x_sector(get_race_from_args(args))

def generate_x_character(args):
    #TODO: support arguments similar to generate_name()
    return xnames.flatten("#origin#")

def generate_dw_character(args):
    #TODO: support arguments similar to generate_name()
    return dungeonworld.flatten("#origin#")

def generate_dwpw_region(args):
    return dwpw.flatten("#region#")

def generate_dwpw_place(args):
    return dwpw.flatten("#place#")

def generate_elder_god(args):
    #TODO: support arguments similar to generate_name()
    return eldergod.flatten("#origin#")

def generate_x_patch(start):
    if start:
        return xpatchmodel.make_sentence_with_start(start)
    else:
        return xpatchmodel.make_sentence()
