#----------------------- DEPENDENCIES ------------------------------
import numpy as np
import random as r
from Simulate import *
from Evolve import *
from Settings import settings
from Backup import *
from Graphing import *
from datetime import datetime
import os
from minor_functions import *
from copy import deepcopy

# sets output & backup folders
outputdir = 'Output5'
backupdir = 'Backup5'
# makes the folders if they don't already exist
if not os.path.isdir(outputdir):
    os.makedirs(outputdir)
if not os.path.isdir(backupdir):
    os.makedirs(backupdir)
# removes pre-existing files in those folders





def run(robots = None, epoch_init = 1, repeatCt=None, lastBestCt=None):


    if epoch_init == 1:
        # clearing Output folder and starting new txt file to hold output if it's the first epoch.
        # if not the first epoch that means we're building off a previous run & want to keep the old files
        for file in os.scandir(outputdir):
            os.remove(file.path)
        for file in os.scandir(backupdir):
            os.remove(file.path)
        f = open(f"{outputdir}/output.txt", 'w')
        f.close()

        # Creating first generation of bots if none were inputted
        robots = create_pop()

    # Going to use these to graph the avg fitness of generations over time
    if repeatCt == None or lastBestCt == None:
        repeatCt, lastBestCt = [], []

    # Cycling through each epoch
    for epoch in range(epoch_init,settings['epochs']+1): # epoch_init is not 1 only if we start from a backup

        #sets an np.array that will be used to get fitness values later on
        # I'm using a normal distribution for the first generation
        if epoch == 1 and settings['dim_range'] == 10:
            fit = [0, 1, 3, 6, 9, 10, 9, 6, 3, 1, 0]
        elif epoch == 1 and settings['dim_range'] == 20:
            fit = [0, 0, 1, 1, 2, 2, 3, 6, 9, 10, 10, 10, 9, 6, 3, 2, 2, 1, 1, 0, 0]
        else: # and then a random gaussian distribution for every following generation
            fit = np.random.randint(0,11,settings['dim_range']+1)
            fit[0], fit[-1] = 0,0 # this is the part that makes it Gaussian (needs to approach zero as it goes to inf & -inf)
        fitsum = sum(fit) # use to standardize the graph across epochs

        now = datetime.now() # recording time so I can estimate how long simulation will take
        current_time = now.strftime("%H:%M:%S")
        f = open(f'{outputdir}/output.txt', 'a')
        f.write(f"BEGIN EPOCH {epoch}\n{fit}\nCurrent Time ={current_time}\n")
        f.close() # recording what's happening in a txt file

        if epoch == 1: # need more gens in first epoch to give decision function time to mature
            generations = settings['first_gens']
        else: # in following generations we need less gens since decision function is pretty much already fully formed
            generations = settings['gens']

        # going through each generation in this epoch
        for gen in range(generations):

            # Simulate all their gaames
            robots = simulate(fit, robots)

            # sort bots
            robots_sorted = sorted(robots, key=operator.attrgetter('avg_fit'), reverse=True)  # puts most fit up front

            # record their stats
            stats = recordStats(robots_sorted, epoch, gen)

            # print out what's happening
            if gen % settings['print_freq'] == 0 or gen == settings['gens']-1 or gen == settings['first_gens']-1:
                out = f">>> EPOCH: {epoch:4}, GEN:{gen : 4}, BEST:{round(stats['fit'], 2) : 7}, AVG:{round(stats['AVG'], 2) : 7}"
                print(out) # print into command line
                f = open(f'{outputdir}/output.txt', 'a') # write into a txt file
                f.write(out+'\n')
                f.close()

            # graph the best robot's grid, path, sen, and per functions on the last gen of each epoch
            if (gen == settings['gens']-1 and epoch > 1) or (gen == settings['first_gens']-1 and epoch == 1):
                graphShit(fit, stats, gen, epoch, outputdir)

            # Evolve (kill off, breed, mutate)
            robots = evolve(robots_sorted)



        # Finding how many sensation repeats the best bot has in the last gen
        repCt = 0
        for j in range(len(L)):  # for all the possible sensation letters
            ct = 0
            for i in range(settings['dim_range'] + 1):
                if stats[str(i)] == L[j]:
                    ct += 1
            if ct > 1:
                repCt += ct - 1

        # Recording number of sensation repeats and the relative fitness success
        repeatCt.append(repCt)
        lastBestCt.append(stats['fit'] / fitsum)

        if len(repeatCt) > 1:
            graphCorr(np.asarray(repeatCt), np.asarray(lastBestCt), outputdir)
            graphRepeat(np.asarray(repeatCt), outputdir)

        # backs up last gen of current epoch into Backup folder
        backupBots(robots, epoch, backupdir)
        # backs up data for fitness over time graph and scatterplot
        backupData(repeatCt, lastBestCt, backupdir)

        # this is set so I only ever have two backups on hand
        if epoch > 2:
            delBackup(epoch-2, backupdir)

    return robots, deepcopy(settings['epochs']), repeatCt, lastBestCt

#reusable_gen, epoch, repeatCt, lastBestCt = run() # I save the gen & epoch in case the simulation ends up needing more epochs than I thought it would

# to reuse the final generation from the final epoch
#reusable_gen, epoch, repeatCt, lastBestCt = run(reusable_gen, epoch, repeatCt, lastBestCt)

# to reuse the generation from the last backup
reusable_gen, epoch, repeatCt, lastBestCt = loadBackup(115, backupdir) # INSERT EPOCH NUMBER MANUALLY HERE
reusable_gen, epoch, repeatCt, lastBestCt = run(reusable_gen, epoch, repeatCt, lastBestCt)
# REMEMBER TO SAVE YOUR OUTPUT FOLDER

# to delete a SPECIFIC backup
#delBackup(15, backupdir) # INSERT EPOCH NUMBER MANUALLY HERE

# To delete ENTIRE Backup folder
#for file in os.scandir(backupdir):
#    os.remove(file.path)

# to graph scatterplot from backed up repeatct list
#reusable_gen, epoch_new, repeatCt, lastBestCt = loadBackup(6, backupdir) # INSERT EPOCH NUMBER MANUALLY HERE
#graphCorr(repeatCt, lastBestCt, outputdir)
#graphRepeat(repeatCt, outputdir)

