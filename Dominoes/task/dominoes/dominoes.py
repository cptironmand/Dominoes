"""
This program will create a set of dominoes, split them up between stock, computer, player,
ID the snake, determine who goes first, and output the variables.
"""


# generate random integer values
from random import randint

# build global variables
starter_piece = []
game_turn = ""


def build_dominoes():
    """
    Create the dominoes and their defaults, and put them into a dictionary
    """
    # Create the dominoes.
    stack = []
    for i in range(0, 7):
        for j in range(0, 7):
            var = [i, j]
            if ([i, j] in stack) or ([j, i] in stack):
                pass
            else:
                stack.append(var)

    # Build the default domino values.  They are 'assigned' to 'none', have not been played, and default as not a snake.
    working_dict = {}

    key = {'assigned'}
    value = 'none'
    new_dict = dict.fromkeys(key, value)
    working_dict.update(new_dict)

    key = {'played'}
    value = False
    new_dict = dict.fromkeys(key, value)
    working_dict.update(new_dict)

    key = {'snake'}
    value = False
    new_dict = dict.fromkeys(key, value)
    working_dict.update(new_dict)

    # Create the dictionary of dominoes
    dominoes = {}
    ind = 0
    for i in stack:
        key = {'value'}
        value = i
        inside_dict = dict.fromkeys(key, value)
        inside_dict.update(working_dict)

        key = {ind}
        value = inside_dict
        outside_dict = dict.fromkeys(key, value)
        dominoes.update(outside_dict)
        ind += 1

    # ID the possible snakes and assign them their value equal to one of the digits
    for i in dominoes:
        if dominoes[i]['value'][0] == dominoes[i]['value'][1]:
            dominoes[i]['snake'] = dominoes[i]['value'][0]
    return dominoes


def shuffle_dominoes(dominoes):
    """
    Randomly assign the dominoes to the computer, the player, and leave the rest in the stock
    """
    picked = []
    num = 1
    while len(picked) < 14:
        secret_value = randint(0, 27)
        if secret_value not in picked:
            picked.append(secret_value)
            if num % 2 == 0:
                dominoes[secret_value]['assigned'] = 'computer'
            else:
                dominoes[secret_value]['assigned'] = 'player'
            num += 1
        else:
            continue
    return dominoes


def assign_stacks(dominoes):
    """
    Take the dominoes as a variable and return the current player, computer, and stock stacks
    """

    count = 0
    stock = []
    computer = []
    player = []
    for i in dominoes:
        if dominoes[i]['assigned'] == 'none':
            stock.append(dominoes[i]['value'])
        elif dominoes[i]['assigned'] == 'computer':
            computer.append(dominoes[i]['value'])
        elif dominoes[i]['assigned'] == 'player':
            player.append(dominoes[i]['value'])
        count += 1

    return player, computer, stock


def first_play(dominoes, snake):
    """
    Find the starter domino (snake), determine which player has it, play the piece, update game pieces
    and return them
    """

    for i in dominoes:
        if dominoes[i]['assigned'] == 'computer':
            if dominoes[i]['snake']:
                snake = ['computer', i]
        elif dominoes[i]['assigned'] == 'player':
            if dominoes[i]['snake']:
                snake = ['player', i]
    dominoes[snake[1]]['assigned'] = 'played'

    if snake[0] == 'player':
        next_turn = 'computer'
    else:
        next_turn = 'player'
    snake = [dominoes[snake[1]]['value']]

    return next_turn, dominoes, snake


def game_screen(player, computer, stock, current, next_turn):
    """
    :param player: player pieces
    :param computer: computer pieces
    :param stock: remaining stock pieces
    :param current: current piece to be played
    :param next_turn: the next player ready to take a turn
    """
    print("======================================================================")
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(computer)}')
    print()
    print(*current)
    print()
    print('Your pieces:')
    num = 1
    for i in range(len(player)):
        print(f'{num}:{player[i]}')
        num += 1
    print()
    if next_turn == 'player':
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")


# --- MAIN BODY OF GAME --- #
game_pieces = build_dominoes()

while not starter_piece:
    game_pieces = shuffle_dominoes(game_pieces)
    game_turn, game_pieces, starter_piece = first_play(game_pieces, starter_piece)

player_pieces, cpu_pieces, remaining_stack = assign_stacks(game_pieces)
game_screen(player_pieces, cpu_pieces, remaining_stack, starter_piece, game_turn)
