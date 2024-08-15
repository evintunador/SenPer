# Anything in here should be here because it gets used in multiple other files
import numpy as np
import numpy.random as r
from Settings import settings
from robot import *


#takes a grid and turns it into fitness values
def convert_to_fit(fit, grid):
    grid = list(grid.flatten())
    for i in range(len(grid)):
        grid[i] = fit[grid[i]]
    grid = np.array(grid).reshape((settings['grid_size'], settings['grid_size']))
    return grid


# Define our Base converter for the decision dictionary
# I got this function from the internet and so have no idea how it actually works
# Its purpose is to turn a base 10 number into its equivalent in base 3 (assuming you chose 2 as the number of
# perception colors)
    # Base 3 rather than 2 because the zero value is used to tell the robot that the grid ends next to it
def int2str(x, base):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if x < 0:
        return "-" + int2str(-x, base)
    return ("" if x < base else int2str(x // base, base)) + digits[x % base]

# just turns a combination from the above function it into a valid world state by adding zeros to the beginning
# (ex: it might come as 101 but I need 00101)
def world_state(x, base):
    combination = int2str(x, base)
    while len(combination) < 5:
        combination = '0' + combination
    return combination

# Putting all the possible world-states into a list
combinations = [None] * ((settings['per_range'] + 1) ** 5)  # number of possible perceptual combinations
for i in range(len(combinations)):
    combinations[i] = world_state(i, settings['per_range' ] +1)

# Removing the ones that make no sense (don't get used)
# the ones where the robot would have to be off the grid
list_to_remove = []
for i in range(len(combinations)):
    if combinations[i][4] == '0':
        list_to_remove.append(combinations[i])
for i in list_to_remove:
        combinations.remove(i)
# removing the ones where the robot would have to be surrounded by the edge of the grid on three or more sides (max possible is 2)
list_to_remove = []
for i in range(len(combinations)):
    test = []
    for j in range(len(combinations[i])):
        if combinations[i][j] == '0':
            test.append(0)
    if len(test) > 2:
        list_to_remove.append(combinations[i])
for i in list_to_remove:
    combinations.remove(i)
# now we have a list of all the possible combinations the robot could perceive (total of 144 in the case of 2 perception colors)


L = 'abcdefghijklmnopqrstuvwxyz'
C = 'brygmckw' # possible colors (matplotlib uses b for blue, r for red, etc

# list of decisions to assign
decisions = ['right', 'left', 'up', 'down', 'pickup', 'stay']
if settings['include_ran'] == True:
    decisions.append('random')


# creates one new robot from scratch. Notice how the key elements of a robot are its perception & decision function
    # the other attributes of a robot don't really matter
def create_new_bot():
    sen_init = {}  # Creating Sensation Function
    for j in range(settings['dim_range'] + 1):
        # maps numbers (corresponding to points on grid) to letters
        sen_init[str(j)] = L[r.randint(0,settings['sen_range'])]

    per_init = {} # Creating Perception Function
    for j in range(settings['sen_range']):
        # maps letters (corresponding to sensation) to colors
        per_init[L[j]] = C[r.randint(0,settings['per_range'])]

    dec_init = {} # Creating Decision Function
    for c in combinations:
        # maps potential world-states (from perception) to decisions
        dec_init[c] = r.choice(decisions)

    return sen_init, per_init, dec_init

# creates a bunch of new robots with totally random per/dec functions
def create_pop():
    robots = [None]*settings['pop_size']
    for i in range(settings['pop_size']):
        sen_init, per_init, dec_init = create_new_bot()
        robots[i] = robot(sen=sen_init, per=per_init, dec=dec_init)
    return robots


def recordStats(robots_sorted, epoch, gen):
    stats = {}

    # recording average fitness of the generation
    ct = 0
    for bot in robots_sorted:
        ct += bot.avg_fit
    stats['AVG'] = ct / len(robots_sorted)

    # best robot's average fitness
    stats['fit']= robots_sorted[0].avg_fit

    # records data useful for graphing if it's the last gen of an epoch
    if (gen == settings['gens'] - 1 and epoch > 1) or (gen == settings['first_gens'] - 1 and epoch == 1):
        # best robot's sensation, perception and decision functions (to be graphed)
        for i in range(settings['dim_range'] + 1):
            stats[str(i)] = robots_sorted[0].sen_fun(i)
        for i in range(settings['sen_range']):
            stats[L[i]] = robots_sorted[0].per_fun(L[i])
        for c in combinations:
            stats[c] = robots_sorted[0].dec_fun(c)

        # other stuff to graph from best robot
        stats['grid_init'] = robots_sorted[0].best_grid_init
        stats['walk'] = robots_sorted[0].best_walk
        stats['grid_fin'] = robots_sorted[0].best_grid_fin
        stats['best_game'] = robots_sorted[0].best_fit
        stats['rand_ct'] = robots_sorted[0].rand_ct

    return stats










#if settings['dim_range'] == 10:
#    uni = [0,1,3,6,9,10,9,6,3,1,0] # 48
#    uniLeft = [0,1,7,14,11,7,4,2,1,1,0]
#    uniRight = [0,0,1,1,2,4,7,11,14,7,1]
#    bi = [0,6,12,5,1,0,1,5,12,6,0]
#    biLeft = [0,8,16,6,1,0,1,4,8,4,0]
#    biRight = [0,4,8,4,1,0,1,6,16,8,0]
#    tri = [0,3,9,4,0,9,8,0,4,9,3]
#    triAscend = [0,2,5,2,4,9,4,0,6,11,6]
#    triDescend = [0,6,11,6,4,9,4,0,2,5,2]
#    triMidSmall = [0,5,10,5,2,5,2,0,5,10,5]
#    triMidBig = [0,3,7,3,6,11,6,0,3,7,3]
#elif settings['dim_range'] == 20:
#    uni =           [0, 0, 1, 1, 2, 2, 3, 6, 9, 10, 10, 10, 9, 6, 3, 2, 2, 1, 1, 0, 0] # 78
#    uniLeft =       [0, 1, 3, 6, 9, 10, 10, 9, 8, 6, 4, 3, 2, 2, 1, 1, 1, 1, 0, 0, 0]
#    uniRight =      [0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 4, 6, 8, 9, 10, 10, 9, 6, 3, 1, 0]
#    bi =            [0, 1, 2, 5, 7, 9, 7, 5, 2, 1, 0, 1, 2, 5, 7, 9, 7, 5, 2, 1, 0]
#    biLeft =        [0, 1, 4, 7, 9, 11, 9, 7, 4, 1, 0, 0, 1, 3, 5, 7, 5, 3, 1, 0, 0]
#    biRight =       [0, 0, 1, 3, 5, 7, 5, 3, 1, 0, 0, 1, 4, 7, 9, 11, 9, 7, 4, 1, 0]
#    tri =           [0, 1, 2, 5, 7, 7, 5, 2, 1, 5, 8, 5, 1, 0, 2, 5, 7, 7, 5, 2, 1]
#    triAscend =     [0, 1, 4, 6, 4, 1, 0, 1, 5, 8, 5, 1, 0, 1, 4, 7, 9, 9, 7, 4, 1]
#    triDescend =    [0, 1, 4, 7, 9, 9, 7, 4, 1, 1, 5, 8, 5, 1, 0, 1, 4, 6, 4, 1, 0]
#    triMidSmall =   [0, 1, 4, 7, 8, 7, 4, 1, 1, 4, 4, 4, 1, 0, 1, 4, 7, 8, 7, 4, 1]
#    triMidBig =     [0, 1, 4, 7, 4, 1, 0, 2, 6, 9, 10, 9, 6, 2, 0, 1, 4, 7, 4, 1, 0]
#else:
#    raise Exception ("dim_range needs to be either 10 or 20")

#sets the relative frequency of each fitness function
#functions = [uni, uni, uni, uni, uniLeft, uniLeft, uniLeft, uniRight, uniRight, uniRight, bi, bi, bi, biLeft, \
#            biLeft, biRight, biRight, tri, tri, triAscend, triDescend, triMidSmall, triMidBig]




# RETURNS NORMAL DISTRIBUTION VALUE
#def norm(x, mu, sig, h):
#    return (h / np.sqrt(2 * np.pi)) * np.exp((-.5) * (((x - mu) / sig) ** 2))
# UNIMODAL
#def uni(x):
#    return norm(x, (10 / 20) * settings['dim_range'], (3 / 20) * settings['dim_range'], 24)
#def uni_left(x):
#    return norm(x, (13 / 20) * settings['dim_range'], (3 / 20) * settings['dim_range'], 12) + \
#           norm(x, (15 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 12) + \
#           norm(x, (11 / 20) * settings['dim_range'], (3 / 20) * settings['dim_range'], 2)
#def uni_right(x):
#    return norm(x, (7 / 20) * settings['dim_range'], (3 / 20) * settings['dim_range'], 12) + \
#           norm(x, (5 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 12) + \
#           norm(x, (9 / 20) * settings['dim_range'], (3 / 20) * settings['dim_range'], 2)
# BIMODAL
#def bi(x):
#    return norm(x, (5 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 24) + \
#           norm(x, (15 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 24)
#def bi_leftBig(x):
#    return norm(x, (5 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 30) + \
#           norm(x, (15 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 18)
#def bi_rightBig(x):
#    return norm(x, (5 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 18) + \
#           norm(x, (15 / 20) * settings['dim_range'], (1.5 / 20) * settings['dim_range'], 30)
# TRIMODAL
#def tri(x):
#    return norm(x, (3.5 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 24) + \
#           norm(x, (10 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 24) + \
#           norm(x, (16.5 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 24)
#def tri_ascend(x):
#    return norm(x, (4 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 16) + \
#           norm(x, (10 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 24) + \
#           norm(x, (16 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 32)
#def tri_descend(x):
#    return norm(x, (4 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 32) + \
#           norm(x, (10 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 24) + \
#           norm(x, (16 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 16)
#def tri_midSmall(x):
##    return norm(x, (4 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 30) + \
#           norm(x, (10 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 18) + \
#           norm(x, (16 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 30)
#ef tri_midBig(x):
#    return norm(x, (4 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 18) + \
#           norm(x, (10 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 30) + \
#           norm(x, (16 / 20) * settings['dim_range'], (1 / 20) * settings['dim_range'], 18)

# the following comment belongs in main.py
# to call the continuous version you do functions[z](x)
