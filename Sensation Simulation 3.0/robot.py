from Settings import settings

C = 'brygmckw'

# -------------------------------- CLASS ----------------------------
class robot:
    def __init__(self, sen, per, dec):
        #self.x = x
        #self.y = y
        # todo I removed the x and y here but I'm not sure I should've , x = None, y = None

        # the robot saves what happened on its highscore so that can be graphed later
        self.best_walk = [None] * settings['tries']
        self.best_grid_init = []
        self.best_grid_fin = []
        self.best_fit = None
        self.avg_fit = None # also saves its average fitness level

        self.sen = sen
        self.per = per
        self.dec = dec

        # if you do choose to include 'random' as a decision choice, then I keep track of how often the bot
        # chooses to act randomly. I think if it happens too often that's a failure
        self.rand_ct = 0

    # so you can later get the robot's perception. Takes a number 0-10 as input
    def sen_fun(self, i):
        return self.sen[str(i)]  # needs an integer as an input

    # needs a five-digit number with the right base as an input
    def per_fun(self, i):
        return self.per[str(i)]

    # needs a stringed number with the right base as an input
    def dec_fun(self, i):
        return self.dec[str(i)]

    # Decision Maker
    def think(self, grid, y, x):

        for i in range(settings['per_range']):
            if y == settings['grid_size'] - 1: # if the robot is up against the edge of the grid
                dig1 = 0 # zero represents the cliff
            elif self.per[self.sen[str(grid[y + 1][x])]] == C[i]: # if the space below the bot is the given color
                dig1 = i + 1

            if y == 0:
                dig2 = 0
            elif self.per[self.sen[str(grid[y - 1][x])]] == C[i]:
                dig2 = i + 1

            if x == settings['grid_size'] - 1:
                dig3 = 0
            elif self.per[self.sen[str(grid[y][x + 1])]] == C[i]:
                dig3 = i + 1

            if x == 0:
                dig4 = 0
            elif self.per[self.sen[str(grid[y][x - 1])]] == C[i]:
                dig4 = i + 1

            # we don't need to check for being off the grid on this one because this is the point the robot
            # is actually on
            if self.per[self.sen[str(grid[y][x])]] == C[i]: dig5 = i + 1

        # now that we have the world-state, we can see what the decision funtion wants to do
        decision = self.dec[f"{dig1}{dig2}{dig3}{dig4}{dig5}"]

        return decision