import matplotlib.pyplot as plt
from Settings import settings
from minor_functions import *

C = 'brygmckw'
L = 'abcdefghijklmnopqrstuvwxyz'
sen_col_conv = {'a':'b', 'b':'r', 'c':'y', 'd':'g', 'e':'m', 'f':'c', 'g':'k', 'h':'lightgray', 'i':'darkorange',\
                'j':'tab:brown', 'k':'tab:gray', 'l':'peru', 'm':'greenyellow', 'n':'tab:blue', 'o':'navy', 'p':'indigo', \
                'q':'lightpink', 'r':'darkcyan', 's':'olive', 't':'lightsteelblue'}

# sets up all the lists needed to plot the robot's pathway through the grid
def plot_path(walk: list):
    x = [0] * len(walk)  # records position over time
    y = [0] * len(walk)
    x[0] = int(walk[0].split(',')[0])  # sets initial position
    y[0] = int(walk[0].split(',')[1])

    pickupsx, pickupsy = [], []  # records points at which robot picks up
    staysx, staysy = [], []  # records points at which robot chooses to stay
    cliffx, cliffy = [], []  # records points at which robot tries to walk off the edge

    for i in range(1, len(walk)): # starts at 1 because the 0 index in the list holds the robot's initial position
        if walk[i] == 'left' and x[i - 1] != 0: # these second parts of the conditionals prevent the graph from walking off the grid
            x[i] = x[i - 1] - 1
            y[i] = y[i - 1]
        elif walk[i] == 'right' and x[i - 1] != settings['grid_size'] - 1:
            x[i] = x[i - 1] + 1
            y[i] = y[i - 1]
        elif walk[i] == 'up' and y[i - 1] != 0:
            x[i] = x[i - 1]
            y[i] = y[i - 1] - 1
        elif walk[i] == 'down' and y[i - 1] != settings['grid_size'] - 1:
            x[i] = x[i - 1]
            y[i] = y[i - 1] + 1
        elif walk[i] == 'stay':
            x[i] = x[i - 1]
            y[i] = y[i - 1]
            staysx.append(x[i])
            staysy.append(y[i])
        elif walk[i] == 'pickup':
            x[i] = x[i - 1]
            y[i] = y[i - 1]
            pickupsx.append(x[i])
            pickupsy.append(y[i])
        else:
            x[i] = x[i - 1]
            y[i] = y[i - 1]
            cliffx.append(x[i])
            cliffy.append(y[i])

    return x, y, staysx, staysy, pickupsx, pickupsy, cliffx, cliffy

# Returns values allowing to plot sensation function as a bar chart
def plot_sen(stats):
    col_sen = [None]*(settings['dim_range'] + 1)
    for i in range(settings['dim_range'] + 1):
        # stats[i] pumps out a letter of alphabet adn sen_col_conv[L] pumps out a usable color for matplotlib
        col_sen[i] = f"{sen_col_conv[stats[str(i)]]}"
    return col_sen

# Returns values allowing to plot perception function as a bar chart
def plot_per(stats):
    col_per = [None]*(settings['dim_range']+1)
    for i in range(settings['dim_range']+1):
        col_per[i] = f"{stats[stats[str(i)]]}"
    return col_per

# graphs the grids, robot's path, and robot's sen & per functions
def graphShit(fit, stats, gen, epoch, outputdir):
    # Setup for grids
    grid_init = convert_to_fit(fit, stats['grid_init'])
    grid_fin = convert_to_fit(fit, stats['grid_fin'])
    x_list, y_list, staysx, staysy, pickupsx, pickupsy, cliffx, cliffy = plot_path(stats['walk'])

    # setup for sen & per bar charts
    dim_range = list(range(settings['dim_range'] + 1))
    sen_col = plot_sen(stats)
    per_col = plot_per(stats)

    fig = plt.figure()

    # Initial Grid + path
    ax1 = plt.subplot2grid((7, 4), (0, 0), colspan=2, rowspan=4)
    ax1.matshow(grid_init)
    ax1.plot(x_list, y_list, 'r-')
    ax1.plot(x_list[0], y_list[0], 'rd')
    ax1.plot(x_list[-1], y_list[-1], 'rs')
    ax1.plot(staysx, staysy, 'g.')
    ax1.plot(pickupsx, pickupsy, 'y.')
    ax1.plot(cliffx, cliffy, 'wx')

    # Final Grid + path
    ax2 = plt.subplot2grid((7, 4), (0, 2), colspan=2, rowspan=4)
    ax2.matshow(grid_fin)
    ax2.plot(x_list, y_list, 'r-')
    ax2.plot(x_list[0], y_list[0], 'rd')
    ax2.plot(x_list[-1], y_list[-1], 'rs')
    ax2.plot(staysx, staysy, 'g.')
    ax2.plot(pickupsx, pickupsy, 'y.')
    ax2.plot(cliffx, cliffy, 'wx')

    # Perception Function
    ax3 = plt.subplot2grid((7, 4), (4, 0), colspan=4, rowspan=2)
    ax3.bar(dim_range, [max(fit)] * (settings['dim_range'] + 1), color=per_col)
    ax3.plot(range(settings['dim_range'] + 1), fit, 'black')
    ax3.get_xaxis().set_visible(False)

    # Sensation Function
    ax4 = plt.subplot2grid((7, 4), (6, 0), colspan=4)
    ax4.bar(dim_range, [1] * (settings['dim_range'] + 1), color=sen_col)
    ax4.get_yaxis().set_visible(False)

    plt.xlabel(f"This robot is from epoch {epoch} gen {gen}, highscore {round(stats['best_game'], 2)}, avg {round(stats['fit'], 2)}, and chose random {stats['rand_ct']} times")
    #fig.show()
    fig.savefig(f"{outputdir}/Path_epoch{epoch}gen{gen}.jpg", bbox_inches='tight', pad_inches=.1, dpi=600)
    fig.clf()
    plt.close('all')

# graphs the avg fitness and fitness of best bot of each gen over time. Should dip at each new epoch then climb back up
#def graphFit(avg, best, epoch, outputdir):
#   length = settings['first_gens'] + settings['gens']*(epoch-1)
#    plt.figure(figsize=(20, 5))

    # vertical lines at each epoch
#    plt.axvline(x=settings['first_gens']-1, color = 'lightgrey')
#    for i in range(2,epoch+1):
#        plt.axvline(x=settings['first_gens']-1 + (i-1)*settings['gens'], color = 'lightgrey')

#    plt.plot(range(length), avg, 'r-', label = 'Average')
#    plt.plot(range(length), best, 'b-', label = 'Best')

    # x-axis
#    plt.plot(range(length), [0]*length, 'black', label = None)

 #   plt.ylabel('Fitness')
#    plt.xlabel('Generation')
#    plt.legend()
    
#    plt.savefig(f"{outputdir}/FitnessOverTime.jpg", bbox_inches='tight', pad_inches=.1, dpi=600)
#    #plt.show()
#    plt.close('all')

def graphCorr(repeat, success, outputdir):
    plt.scatter(repeat, success)

    plt.ylabel('Relative Success')
    plt.xlabel('Number of Repeats')

    plt.savefig(f"{outputdir}/RelativeSuccess.jpg", bbox_inches='tight', pad_inches=.1, dpi=600)
    plt.close('all')

def graphRepeat(repeat, outputdir):
    plt.figure(figsize=(15, 5))

    plt.plot(range(len(repeat)), repeat)
    plt.ylabel('Number of Repeats')
    plt.xlabel('Epoch')

    plt.savefig(f"{outputdir}/Repeats.jpg", bbox_inches='tight', pad_inches = .1, dpi=600)
    plt.close('all')