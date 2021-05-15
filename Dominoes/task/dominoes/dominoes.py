"""
This program will create a set of dominoes, split them up between stock, computer, player,
ID the snake, determine who goes first, and output the variables.
"""

import random
from random import randint
import collections

# build global variables
played_doms = collections.deque()
game_turn = ""
game_over = False


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
    value = False
    new_dict = dict.fromkeys(key, value)
    working_dict.update(new_dict)

    #key = {'played'}
    #value = False
    #new_dict = dict.fromkeys(key, value)
    #working_dict.update(new_dict)

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
    unplayed = []
    computer = []
    player = []
    player_out = []
    computer_out = []
    for i in dominoes:
        if not dominoes[i]['assigned']:
            unplayed.append(i)
        elif dominoes[i]['assigned'] == 'computer':
            computer.append(i)
        elif dominoes[i]['assigned'] == 'player':
            player.append(i)
        count += 1

    cnt = 1
    for i in range(len(computer)):
        computer_out.append([cnt, computer[i]])
        cnt += 1

    cnt = 1
    for i in range(len(player)):
        player_out.append([cnt, player[i]])
        cnt += 1

    return player_out, computer_out, unplayed


def first_play(dominoes, played):
    """
    Find the starter domino (snake), determine which player has it, play the piece, update game pieces
    and return them
    """

    temp_played = []
    for i in dominoes:
        if dominoes[i]['assigned'] == 'computer':
            if dominoes[i]['snake']:
                temp_played = ['computer', i]
        elif dominoes[i]['assigned'] == 'player':
            if dominoes[i]['snake']:
                temp_played = ['player', i]
    dominoes[temp_played[1]]['assigned'] = 'played'

    if temp_played[0] == 'player':
        next_turn = 'computer'
    else:
        next_turn = 'player'
    played.append(dominoes[temp_played[1]]['value'])

    return next_turn, dominoes, played


def cpu_turn(dominoes, played):
    """CPU turn; play an available domino or pick one"""

    # Find left and right most played numbers
    left = played[0][0]
    length = len(played)
    right = played[length-1][1]

    # Determine if computer has a playable domino in their stack
    playable = False
    length = len(played)

    for i in dominoes:
        if dominoes[i]['assigned'] == 'computer':
            if left == dominoes[i]['value'][1]:
                played.appendleft(dominoes[i]['value'])
            elif left == dominoes[i]['rev_value'][1]:
                played.appendleft(dominoes[i]['rev_value'])
            elif right == dominoes[i]['value'][0]:
                played.append(dominoes[i]['value'])
            elif right == dominoes[i]['rev_value'][0]:
                played.append(dominoes[i]['rev_value'])

            if len(played) > length:
                dominoes[i]['assigned'] = 'played'
                playable = True
                break

    # Draw a new domino if no playable domino in stack exists
    if not playable:
        draw_pile = []
        for i in dominoes:
            if not dominoes[i]['assigned']:
                draw_pile.append(i)
        pick = random.choice(draw_pile)
        dominoes[pick]['assigned'] = 'computer'

    turn = 'player'

    return dominoes, played, turn


def game_screen(player, computer, stock, played, turn, dominoes):
    """
    Create the game screen and display the output
    """
    print("======================================================================")
    print(f'Stock size: {len(stock)}')
    print(f'Computer pieces: {len(computer)}')
    #print(f'pieces are: {computer}')
    print()
    print(*played)
    print()
    print('Your pieces:')
    for i in range(len(player)):
        print(f'{player[i][0]}: {dominoes[player[i][1]]["value"]}')
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
game_screen(player_doms, cpu_doms, unplayed_doms, played_doms, game_turn, dominoes_dict)

dominoes_dict, played_doms, game_turn = cpu_turn(dominoes_dict, played_doms)
player_doms, cpu_doms, unplayed_doms = update_stacks(dominoes_dict)
game_screen(player_doms, cpu_doms, unplayed_doms, played_doms, game_turn, dominoes_dict)