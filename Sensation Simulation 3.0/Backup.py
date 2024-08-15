import ast
import os
from Settings import settings
from robot import *

# backs up minimum info necessaray to be able to recreate the generation
# not sure if this is the most efficient way to do this.
def backupBots(robots, epoch, backupdir):
    for bot in range(len(robots)): # goes through each bot
        # saves the disctionaries as txt files
        f = open(f"{backupdir}/epoch[{epoch}]bot[{bot}]sen.txt", 'w') # sensation
        f.write(str(robots[bot].sen))
        f.close()
        f = open(f"{backupdir}/epoch[{epoch}]bot[{bot}]per.txt", 'w') # perception
        f.write(str(robots[bot].per))
        f.close()
        f = open(f"{backupdir}/epoch[{epoch}]bot[{bot}]dec.txt", 'w') # decision
        f.write(str(robots[bot].dec))
        f.close()

def backupData(repeat, lastBest, backupdir):
    f = open(f"{backupdir}/repeatCt.txt",'w')
    f.write(str(repeat))
    f.close()
    f = open(f"{backupdir}/lastBestCt.txt",'w')
    f.write(str(lastBest))
    f.close()

# deletes backup from a specific epoch (in case you don't want to erase the entire Backup folder)
def delBackup(epoch, backupdir):
    for i in range(settings['pop_size']):
        os.remove(f"{backupdir}/epoch[{epoch}]bot[{i}]sen.txt")
        os.remove(f"{backupdir}/epoch[{epoch}]bot[{i}]per.txt")
        os.remove(f"{backupdir}/epoch[{epoch}]bot[{i}]dec.txt")


# loads backup from a specific epoch
def loadBackup(epoch, backupdir):
    epoch_new = epoch+1
    robots = [None] * settings['pop_size'] # if the pop_size gets changed then this function will fuck up

    for i in range(settings['pop_size']):
        file = open(f"{backupdir}/epoch[{epoch}]bot[{i}]sen.txt", "r") # sensation
        sen = ast.literal_eval(file.read())
        file.close()

        file = open(f"{backupdir}/epoch[{epoch}]bot[{i}]per.txt", "r") # perception
        per = ast.literal_eval(file.read())
        file.close()

        file = open(f"{backupdir}/epoch[{epoch}]bot[{i}]dec.txt", "r") # decision
        dec = ast.literal_eval(file.read())
        file.close()

        # now we have a list of robots to return
        robots[i] = robot(sen=sen, per=per, dec=dec)

    # loading for scatterplot
    file = open(f"{backupdir}/repeatCt.txt", 'r')
    rep = ast.literal_eval(file.read())
    file.close()
    file = open(f"{backupdir}/lastBestCt.txt", 'r')
    lastBest = ast.literal_eval(file.read())
    file.close()

    return robots, epoch_new, rep, lastBest