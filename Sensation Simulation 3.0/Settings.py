# ------------------- CONSTANTS / SETTINGS ------------------------
settings = {}
# Very large values are not recommended even for parameters that claim a range to inf

# DEFAULTS:
# 200 robots
# 1000 generations
# 'small' amount of mutation?
# 200 moves
# 100 tries
# 2 colors
# 10 sensation outputs
# no new randos
# idk about elitism
# 1 epoch

# Output / feedback settings
settings['print_freq'] = 25 # how many generations to print the text output
settings['include_ran'] = False # I've chosen not to include the 'random' choice for the robots' actions since it encourages
# a stupid local minimum in the evolutionary optimization where the robot only sees one color and just walks around randomly
# with the exception of knowing not to walk off the walls
settings['asexual'] = True # I don't think this one matters. False for sexual reproduction

# EVOLUTION SETTINGS
settings['pop_size'] = 200  # Population size in each generation (default 200)
settings['first_gens'] = 5000 # number of generations for first epoch (default 8000)
# (needs to be longer than 'gens' in order to do initial training of decision function)
settings['gens'] = 1000  # Number of generations for the rest of the epochs (default 1000)
settings['epochs'] = 1000 # 1000 epochs? or 100? idk yet but hopefully 100 will be enough
settings['elitism'] = .5  # Portion of top robots from previous gen to stay
settings['mutate_sen'] = .00005 # Sensation function's mutation rate ( lower on purpose)
settings['mutate_per'] = .05  # Perception function's mutation rate
settings['mutate_dec'] = .01 # Decision function's mutation rate ( lower because there are more genes in decision function than in pereption)
#it should be noted that these mutation rates are not all exactly equivalent. Each function has a given number of genes, and the mutation
# rate is the probability that each gene will individually mutate when a baby bot is born. However, each function has a different number of genes
# (the decision function has by far the most) which is why the rates aren't all really equivalent

# Simulation Settings
settings['moves'] = 50  # Number of moves a robot gets when in a grid (length of each game) (default 50)
settings['tries'] = 50  # Number of times a robot plays the game (scores will be averaged) (default 50)
settings['punishment'] = 1  # Number of fitness points to negate when hitting edge of board (1 seems to be enough)
settings['grid_size'] = 10  # Size of playable grid (square). I don't think this one should matter (int, 2 to inf)
settings['dim_range'] = 10  # How many units the 'reality' dimension can take (either 10 or 20)

# ORGANISM SENSATION/PERCEPTION SETTINGS
settings['sen_range'] = 11 # number of units (letters) the sensation function can output (int, 2 to 20)
settings['per_range'] = 2  # number of units (colors) the perception function can output (int, 2 to 8)


