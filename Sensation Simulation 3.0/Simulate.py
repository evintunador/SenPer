import random as r
from copy import deepcopy
from minor_functions import *
import numpy as np


decisions = ['left', 'right', 'up', 'down', 'stay', 'pickup']


def act(fit, choice, grid, x, y, fitness_pts):
    # Implements bot's decision
    if choice == 'pickup':
        fitness_pts += fit[grid[y][x]]
        grid[y][x] = 0
    elif choice == 'up' and y > 0: # second condition prevents walking off the grid
        y -= 1
    elif choice == 'down' and y < settings['grid_size'] - 1:
        y += 1
    elif choice == 'left' and x > 0:
        x -= 1
    elif choice == 'right' and x < settings['grid_size'] - 1:
        x += 1
    elif choice != 'stay':
        # if it got all the way down here and its chocie wasn't equal to 'stay' that would mean it walked off grid
        fitness_pts -= settings['punishment']
    #and if its choice was 'stay' then nothing happens

    return grid, x, y, fitness_pts


# playing a single full game
def play(fit, robots, bot):
    # Set up how to score him and track his movements
    fitness_pts = 0
    walkthrough = [None] * (settings['moves'] + 1)
    rand_ct = 0 # I keep track of number of times he chooses random cuz I don't like that

    # Set up Playing Grid & starting position
    grid = r.randint(0, settings['dim_range'] + 1, (settings['grid_size'], settings['grid_size'])) # for some reason this doesn't work in the console
    #grid = np.random.randint(0, settings['dim_range']+1,settings['grid_size']**2).reshape((settings['grid_size'],settings['grid_size']))
    y, x = r.randint(0, settings['grid_size']), r.randint(0, settings['grid_size'])

    # sets up data about bot to be saved
    grid_initial = deepcopy(grid)
    walkthrough[0] = f"{x},{y}"

    # CYCLE THROUGH HOW MANY MOVES HE GETS
    for mov in range(settings['moves']):
        # gets bot's decision & records it
        dec = robots[bot].think(grid, y, x)
        if dec == 'random':
            rand_ct += 1
            dec = r.choice(decisions)
        walkthrough[mov + 1] = dec # records

        # actually implements bot's deicision
        grid, x, y, fitness_pts = act(fit, dec, grid, x, y, fitness_pts)

    # deepcopy the final grid cuz i'm paranoid about python's referencing mechanism
    return grid_initial, walkthrough, fitness_pts, deepcopy(grid), rand_ct


# goes through each robot and each robot plays multiple games
def simulate(fit, robots):
    # CYCLE THROUGH EACH ROBOT
    for bot in range(settings['pop_size']):

        # records the winnings of each game (to be averaged later)
        winnings = [None] * settings['tries']
        # an initial value that I assume each game will do better than. to be used in if statement later
        best_pts = -1e10

        # CYCLE THROUGH HOW MANY TRIES/GAMES THEY GET
        for go in range(settings['tries']):

            # plays the game
            grid_initial, walkthrough, fitness_pts, grid_fin, rand_ct = play(fit, robots, bot)

            # adds the score of that game to the list of scores
            winnings[go] = fitness_pts

            # we're hoping to record only the best game in the end
            if fitness_pts > best_pts:
                best_pts = fitness_pts # updates best_pts to the new high score
                best_grid_init = grid_initial
                best_grid_fin = grid_fin
                best_walk = walkthrough
                best_rand_ct = rand_ct

        robots[bot].best_grid_init = best_grid_init # I really should be making these names more consistent
        robots[bot].best_grid_fin = best_grid_fin
        robots[bot].best_fit = best_pts
        robots[bot].avg_fit = sum(winnings) / len(winnings)
        robots[bot].best_walk = best_walk
        robots[bot].rand_ct = best_rand_ct

    # returns the robots that have now recorded all of their high scores & details of their high score games
    return robots