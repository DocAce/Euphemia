import discord # pylint: disable=import-error
import string
import euphemia_gens
import euphemia_gm
import dicey

punctuation_remover = str.maketrans('', '', string.punctuation)

help_text = ('Thank you for taking an interest in me! I have a list of keywords I respond to which I will list shortly.\n'
             '`-roll` Rolls a number of dice and adds the results together. Please make sure that the entire parameter block does not have internal spaces, and no punctuation directly next to it, thank you! Example: `-roll 3d12+7`\n'
             '`-flip`: Flips a number of coins. Example: `-flip 3`\n'
             '`-generate`: Gives access to a whole bunch of random text generators. You can type the command on its own to get more details.\n'
             '`-help`: You just typed this!')
youre_welcome_text = 'I do not have a memory and thus cannot remember what I did for you. But you are very welcome.'
generate_text = ('To generate some text, type `-generate [generator]`. Some generators accept additional parameters, these will be listed below.\n'
                 'The generators are:\n'
                 '`name`: Creates a random name from the X universe. Accepts a race and/or a gender as parameters. The order of parameters is not important. Example: `-generate split female name`\n'
                 '`sector`: Creates a random sector name from the X universe. Accepts a race as a parameter. Example: `-generate split sector`\n'
                 '`teladiname`, `boronname`, `paranidname`, `splitname`, `splitmalename` and `splitfemalename` are more freeform name generators than the above and can generate output that is not found in X4.\n'
                 '`xchar`: Generate a character for the X universe.\n'
                 '`xpatch`: Generate a patch note for X4.\n'
                 '`x3sector`: Generate a sector description. Often nonsensical.\n'
                 '`dwchar`: Generate a Dungeon World character.\n'
                 '`pwregion`: Generate the name of a region in the Perilous Wilds.\n'
                 '`pwplace`: Generate the name of a place in the Perilous Wilds.\n'
                 '`gmprompt`: Generate a prompt a game master might give a player. Often silly.\n'
                 '`quest`: Generate a quest.\n'
                 '`eldergod`: Generates the name and domain of an elder god. If you read the output do a sanity check.')

async def handle_message(message, bot):
    args = message.content.lower()
    commands = args.translate(punctuation_remover)
    args = args.split(' ')
    commands = commands.split(' ')
    if args[0] == '-help':
        await message.channel.send(help_text)
    elif args[0] == '-game':
        await message.channel.send(euphemia_gm.handle_message(message, commands, args))
    elif args[0] == '-flip':
        await message.channel.send(dicey.generate_coin_flip_output(args))
    elif args[0] == '-roll':
        await message.channel.send(dicey.generate_dice_roll_output(args))
    elif args[0] == '-generate':
        args = args[1:]
        if 'sector' in commands:
            await message.channel.send(euphemia_gens.generate_x_sector_from_args(args))
        elif 'name' in commands:
            await message.channel.send(euphemia_gens.generate_x_name_from_args(args))
        elif 'teladiname' in commands:
            await message.channel.send(euphemia_gens.xnames.flatten('#teladiFullRandomName#'))
        elif 'boronname' in commands:
            await message.channel.send(euphemia_gens.xnames.flatten('#boronFullRandomName#'))
        elif 'paranidname' in commands:
            await message.channel.send(euphemia_gens.xnames.flatten('#paranidFullRandomName#'))
        elif 'splitname' in commands:
            await message.channel.send(euphemia_gens.xnames.flatten('#splitFullRandomName#'))
        elif 'splitmalename' in commands:
            await message.channel.send(euphemia_gens.xnames.flatten('#splitMaleFullRandomName#'))
        elif 'splitfemalename' in commands:
            await message.channel.send(euphemia_gens.xnames.flatten('#splitFemaleFullRandomName#'))
        elif 'xchar' in commands:
            await message.channel.send(euphemia_gens.generate_x_character(args))
        elif 'dwchar' in commands:
            await message.channel.send(euphemia_gens.generate_dw_character(args))
        elif 'pwregion' in commands:
            await message.channel.send(euphemia_gens.dwpw.flatten('#region#'))
        elif 'pwplace' in commands:
            await message.channel.send(euphemia_gens.dwpw.flatten('#place#'))
        elif 'gmprompt' in commands:
            await message.channel.send(euphemia_gens.gmprompt.flatten('#origin#'))
        elif 'quest' in commands:
            await message.channel.send(euphemia_gens.gmprompt.flatten('#quest#'))
        elif 'eldergod' in commands:
            await message.channel.send(euphemia_gens.generate_elder_god(args))
        elif 'xpatch' in commands:
            await message.channel.send(euphemia_gens.generate_x_patch(message.content[17:]))
        elif 'x3sector' in commands:
            await message.channel.send(euphemia_gens.generate_x3_sectordesc(message.content[19:]))
        elif 'x4sector' in commands:
            await message.channel.send(euphemia_gens.generate_x4_sectordesc(message.content[19:]))
        else:
            await message.channel.send(generate_text)
