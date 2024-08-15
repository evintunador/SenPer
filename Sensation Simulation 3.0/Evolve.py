import random as r
from collections import defaultdict
from math import floor
import operator
from minor_functions import *
from robot import *
from Settings import settings


L = 'abcdefghijklmnopqrstuvwxyz'
C = 'brygmckw'
decisions = ['right', 'left', 'up', 'down', 'pickup', 'stay']
if settings['include_ran'] == True:
    decisions.append('random')


def breed(mom, dad):
    sen_new, per_new, dec_new = {}, {}, {}
    crossover_weight = r.random()

    # Making the baby's sensation function out of the two parents chosen
    for i in range(settings['dim_range'] + 1):

        # if asexual, then mom is only parent and dad is ignored
        # if sexual reproduction, then random variable determines which parent the baby bot gets genes from
        if settings['asexual'] == True or (settings['asexual'] == False and r.random() < crossover_weight):
            sen_new[str(i)] = mom.sen[str(i)] # take mom's gene
        else:
            sen_new[str(i)] = dad.sen[str(i)] # take dad's gene

    # Making the baby's perception function out of the two parents chosen
    for i in range(settings['sen_range']):
        if settings['asexual'] == True or (settings['asexual'] == False and r.random() < crossover_weight):
            per_new[L[i]] = mom.per[L[i]]
        else:
            per_new[L[i]] = dad.per[L[i]]

    # Making the baby's decision function out of the two parents chosen
    for c in combinations:
        if settings['asexual'] == True or (settings['asexual'] == False and r.random() < crossover_weight):
            dec_new[c] = mom.dec[c]
        else:
            dec_new[c] = dad.dec[c]

    return sen_new, per_new, dec_new


def mutate(sen, per, dec):
    # sensation mutation
    for i in range(settings['dim_range'] + 1):
        if r.random() < settings['mutate_sen']:
            sen[str(i)] = L[r.randint(0,settings['sen_range'])]

    # perception mutation
    for i in range(settings['sen_range']):
        if r.random() < settings['mutate_per']:
            per[L[i]] = C[r.randint(0,settings['per_range'])]

    # decision mutation
    for c in combinations:
        if r.random() < settings['mutate_dec']:
            dec[c] = r.choice(decisions)

    return sen, per, dec


def evolve(robots):

    # how many new bots we'll have
    robots_new = [None]*settings['pop_size']
    # How many get to survive (elitism)?
    elitism_num = int(floor(settings['elitism'] * settings['pop_size']))
    # how many we have to replace (create)
    babies_num = settings['pop_size'] - elitism_num

    # Making winners go to next gen (they're already sorted form best to worst)
    for i in range(elitism_num):
        robots_new[i] = robot(sen=robots[i].sen, per=robots[i].per, dec=robots[i].dec)

    # Making babies
    for b in range(babies_num):

        # choosing breeding matchup
        bot_1 = robots[r.randint(0,elitism_num)] #mom
        bot_2 = robots[r.randint(0,elitism_num)] #dad
        # reassigns dad to prevent asexual reproduction
        while bot_1 == bot_2 and settings['asexual'] == False:
            bot_2 = robots[r.randint(0, elitism_num)]  # dad

        # Making them fuuuuck (or just asexual reproduction and ignoring bot_2)
        sen_new, per_new, dec_new = breed(bot_1, bot_2)

        # MUTATE THE Babies
        sen_new, per_new, dec_new = mutate(sen_new, per_new, dec_new)

        # Adding the baby to the population
        robots_new[elitism_num + b] = robot(sen=sen_new, per=per_new, dec=dec_new)

    # OUTPUTTING THE NEW GENERATION OF ROBOTS AS WELL AS THEIR STATS
    return robots_new