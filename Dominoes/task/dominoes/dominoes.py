'''
This program will create a set of dominoes, split them up between stock, computer, player,
ID the snake, determine who goes first, and output the variables.
'''

# generate random integer values
from random import randint

# generate a random integer
secret_value = randint(1, 28)


class Domino:
    # list of all dominoes
    all_dominoes = []

    def __init__(self, index_num, value, assigned='stock', played=False):
        self.index_num = index_num
        self.value = value
        self.assigned = assigned
        self.played = played
        # add current river to the list of all rivers
        Domino.all_dominoes.append(self)

# Create the dominoes.  Assign each an index, whether it's been played, who owns it, and the piece value
dominoes = []
stack = []
ind = 0
for i in range(0, 7):
    for j in range(0, 7):
        var = [i, j]
        if ([i, j] in stack) or ([j, i] in stack):
            pass
        else:
            stack.append(var)
            dominoes.append([ind, False, 'stock', var])
            ind +=1



