"""
This program will create a set of dominoes, split them up between stock, computer, player,
ID the snake, determine who goes first, and output the variables.
"""


from random import randint
import collections

# build global variables
played_doms = []
game_turn = ""
game_over = False

in_game_snake_deque = collections.deque()
updated_deque = collections.deque()



def build_dominoes():
    """
    Create the dominoes and their defaults, and put them into a dictionary
    """
    # Create the dominoes.
    stack = []
    rev_stack = []
    for i in range(0, 7):
        for j in range(0, 7):
            var = [i, j]
            rev_var = [j, i]
            if ([i, j] in stack) or ([j, i] in stack):
                pass
            else:
                stack.append(var)
                rev_stack.append(rev_var)

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
        inside_dict1 = dict.fromkeys(key, value)
        inside_dict1.update(working_dict)

        key = {'rev_value'}
        rl = [i[1], i[0]]
        value = rl
        inside_dict2 = dict.fromkeys(key, value)
        inside_dict1.update(inside_dict2)

        key = {ind}
        value = inside_dict1
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


def update_stacks(dominoes):
    """
    Take the dominoes as a variable and return the current player, computer, and stock stacks containing their order
    to be displayed on screen, the value, and the index of that domino in the dictionary
    """

    count = 0
    stock = []
    computer = []
    player = []
    player_out = []
    computer_out = []
    for i in dominoes:
        if dominoes[i]['assigned'] == 'none':
            stock.append(dominoes[i]['value'])
        elif dominoes[i]['assigned'] == 'computer':
            computer.append(dominoes[i]['value'])
        elif dominoes[i]['assigned'] == 'player':
            player.append(dominoes[i]['value'])
        count += 1

    cnt = 1
    for i in range(len(computer)):
        computer_out.append([cnt, computer[i], i])
        cnt += 1

    cnt = 1
    for i in range(len(player)):
        player_out.append([cnt, player[i], i])
        cnt += 1

    return player_out, computer_out, stock


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


def take_turn(player, cpu, unplayed, played, turn):
    """determine the current player, decide whether to pick or play"""

    # Find left and right most played numbers
    left = played[0][0]
    right = played[len(played)][1]

    # Determine if active player has a playable domino in their stack


    # Randomly pick a playable domino if one exists


    # Draw a new domino if no playable domino in stack exists

def game_screen(player, computer, stock, played, turn):
    """
    Create the game screen and display the output
    """
    print("======================================================================")
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(computer)}')
    print()
    print(*played)
    print()
    print('Your pieces:')
    for i in range(len(player)):
        print(f'{player[i][0]}:{player[i][1]}')
    print()
    if turn == 'player':
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")


# --- MAIN BODY OF GAME --- #
dominoes_dict = build_dominoes()

while not played_doms:
    dominoes_dict = shuffle_dominoes(dominoes_dict)
    game_turn, dominoes_dict, played_doms = first_play(dominoes_dict, played_doms)

player_doms, cpu_doms, unplayed_doms = update_stacks(dominoes_dict)
game_screen(player_doms, cpu_doms, unplayed_doms, played_doms, game_turn)
