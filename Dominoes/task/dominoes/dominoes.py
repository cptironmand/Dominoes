"""
This program will create a set of dominoes, split them up between stock, computer, player,
ID the snake, determine who goes first, and output the variables.
"""
# Generate a seed for random number generator
import random
import collections

# build global variables
played_deque = collections.deque()
game_turn = ""
game_winner = False


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

    deck = []
    for i in range(0, 27):
        deck.append(i)
    random.shuffle(deck)
    for i in range(7):
        dominoes[deck.pop()]['assigned'] = 'computer'
        dominoes[deck.pop()]['assigned'] = 'player'

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
    unplayed_out = {}
    player_out = {}
    computer_out = {}
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
        key = {i}
        value = computer[i]
        temp_dict = dict.fromkeys(key, value)
        computer_out.update(temp_dict)
        cnt += 1

    cnt = 1
    for i in range(len(player)):
        key = {i}
        value = player[i]
        temp_dict = dict.fromkeys(key, value)
        player_out.update(temp_dict)
        cnt += 1

    cnt = 1
    for i in range(len(unplayed)):
        key = {i}
        value = unplayed[i]
        temp_dict = dict.fromkeys(key, value)
        unplayed_out.update(temp_dict)
        cnt += 1

    return player_out, computer_out, unplayed_out


def first_play(dominoes, played):
    """
    Find the starter domino (snake), determine which player has it, play the piece, update game pieces
    and return them
    """

    try:
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
    except IndexError:
        print('RAN INTO AN INDEX ERROR')
        next_turn, dominoes, played = first_play(dominoes, played)

    return next_turn, dominoes, played


def cpu_turn(dominoes, played, winner):
    """CPU turn; play an available domino or pick one"""
    cmd = input("Status: Computer is about to make a move. Press Enter to continue...")

    if winner:
        return None

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

        if len(draw_pile) > 0:
            pick = random.choice(draw_pile)
            dominoes[pick]['assigned'] = 'computer'
        else:
            winner = 'draw'

    turn = 'player'
    return dominoes, played, turn, winner


def player_turn(player, dominoes, played, winner):
    """Player turn; play an available domino or pick one"""
    if winner:
        return None

    # Find left and right most played numbers
    left = played[0][0]
    length = len(played)
    right = played[length-1][1]

    pick = False
    print("Status: It's your turn to make a move. Enter your command.\n")
    while not pick:
        cmd = input()
        cmd = int(cmd)
        if cmd == 0:
            draw_pile = []
            for i in dominoes:
                if not dominoes[i]['assigned']:
                    draw_pile.append(i)

            if len(draw_pile) > 0:
                pick = random.choice(draw_pile)
                dominoes[pick]['assigned'] = 'player'
            else:
                winner = 'draw'

        elif cmd > 0:
            ind = player[cmd - 1]
            if right == dominoes[ind]['value'][0]:
                played.append(dominoes[ind]['value'])
                dominoes[ind]['assigned'] = 'played'
            elif right == dominoes[ind]['rev_value'][0]:
                played.append(dominoes[ind]['rev_value'])
                dominoes[ind]['assigned'] = 'played'
            else:
                print("Invalid input. Please try again.")

        elif cmd < 0:
            num = abs(cmd)
            ind = player[num-1]
            if left == dominoes[ind]['value'][1]:
                played.appendleft(dominoes[ind]['value'])
                dominoes[ind]['assigned'] = 'played'
            elif left == dominoes[ind]['rev_value'][1]:
                played.appendleft(dominoes[ind]['rev_value'])
                dominoes[ind]['assigned'] = 'played'
            else:
                print("Invalid input. Please try again.")

        if winner or (length < len(played)):
            pick = True

    turn = 'computer'
    return dominoes, played, turn, winner


def check_winner(player, computer, played, winner):
    if winner:
        return winner

    # Winning Condition 1.a - Player runs out of pieces
    if len(player) < 1:
        winner = 'player'

    # Winning Condition 1.b - CPU runs out of pieces
    if len(computer) < 1:
        winner = 'computer'

    # Draw condition - same end values and appear 8 times
    left = played[0][0]
    length = len(played)
    right = played[length-1][1]
    count = 0
    if left == right:
        for i in played:
            for j in i:
                if j == left:
                    count += 1
    if count == 8:
        winner = 'draw'

    return winner


def game_screen(player, computer, stock, played, turn, dominoes, winner):
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
        print(f'{i+1}:{dominoes[player[i]]["value"]}')
    print()
    if not winner:
        if turn == 'player':
            dominoes, played, turn, winner = player_turn(player, dominoes, played, winner)

        elif turn == 'computer':
            dominoes, played, turn, winner = cpu_turn(dominoes, played, winner)

    if winner:
        if winner == 'player':
            print("Status: The game is over. You won!")
        if winner == 'computer':
            print("Status: The game is over. The computer won!")
        if winner == 'draw':
            print("Status: The game is over. It's a draw!")

    return player, computer, stock, played, turn, dominoes, winner


# --- MAIN BODY OF GAME --- #
doms_dict = build_dominoes()

while not played_deque:
    doms_dict = shuffle_dominoes(doms_dict)
    game_turn, doms_dict, played_deque = first_play(doms_dict, played_deque)

player1, cpu1, unused = update_stacks(doms_dict)
player1, cpu1, unused, played_deque, game_turn, doms_dict, game_winner = game_screen(player1, cpu1, unused,
                                                                                     played_deque, game_turn,
                                                                                     doms_dict, game_winner)


while not game_winner:
    player1, cpu1, unused = update_stacks(doms_dict)
    game_winner = check_winner(player1, cpu1, played_deque, game_winner)
    player1, cpu1, unused, played_deque, game_turn, doms_dict, game_winner = game_screen(player1, cpu1, unused,
                                                                                         played_deque, game_turn,
                                                                                         doms_dict, game_winner)
