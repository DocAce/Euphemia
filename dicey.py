from random import randint

def roll_die(sides):
    return randint(1, sides)

def flip_coin():
    if randint(0, 1) == 0:
        return 'Heads'
    else:
        return 'Tails'

def generate_coin_flip_output(args):
    numflips = 1
    # just use the first number we find as the number of coins to flip
    for arg in args:
        if arg.isdigit():
            numflips = int(arg)
            break
    result = ''
    for i in range(numflips):
        if i > 0:
            result += ', '
        result += flip_coin()
    return result

def generate_dice_roll_output(args):
    numdice = 1
    addsgn = 1
    add = 0
    sides = 6
    # evaluate the first argument that contains the letter d
    # neither the @ nor the command contain that letter, so this should always work
    for arg in args:
        index_d = arg.find('d')
        if index_d > 0:
            rollstring = arg
            # the number in front of the d is how many dice to roll (1 by default)
            numdice = int(rollstring[:index_d])
            rollstring = rollstring[index_d + 1:]
            # either + or -, followed by a number, can be at the end
            index_operator = rollstring.find('+')
            if index_operator == -1:
                index_operator = rollstring.find('-')
                addsgn = -1
            if index_operator != -1:
                add = int(rollstring[index_operator + 1:]) * addsgn
                rollstring = rollstring[:index_operator]
            # if there is a number between the d and the + or - it's the number of sides on the dice (6 by default)
            if rollstring != '':
                sides = int(rollstring)
            break
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
