"""
Clone of 2048 game.
"""


import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    if len(line) <= 1:
        merged_line = line[:]
    else:  
        arranged_line = [0] * (len(line) + 1)
        idx = 0
        for figure in line:
            if figure != 0:
                arranged_line[idx] = figure
                idx += 1
        line1 = arranged_line[:-1]
        line2 = arranged_line[1:]    
        # print(line1,line2)
        merged_line = []
        idx_flag = {idx:True for idx in range(len(line))}
        # print(idx_flag)
        for idx, pair in enumerate(list(zip(line1, line2))):
            # print(idx,pair)
            if idx_flag[idx] == True:
                if pair[0] == pair[1]:
                    merged_figure = pair[0] + pair[1]
                    merged_line.append(merged_figure)
                    idx_flag[idx+1] = False
                else:
                    merged_line.append(pair[0])
                    
                # print(idx_flag)
        merged_line += (len(line) - len(merged_line))*[0]
    return merged_line

def grid_display(grid):
    '''
    show grid in console in a format way (for test)
    '''
    display = ''
    for row in grid:
        for col in row:
            display += ' '
            display += str(col)
        display += '\n'
    return display

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._initial_tiles = {UP:    [(0, col) for col in range(grid_width)],
                               DOWN:  [(grid_height-1, col) for col in range(grid_width)],
                               LEFT:  [(row, 0) for row in range(grid_height)],
                               RIGHT: [(row, grid_width-1) for row in range(grid_height)]}
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)]
                         for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
        # print (self.grid)

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        display = grid_display(self._grid)
        return display


    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        lines = self.get_lines(direction)
        merged_lines = []
        for line in lines:
            merged_line = merge(line)
            merged_lines.append(merged_line)
        original_grid = str(self._grid)
        self.update_grid(direction, merged_lines)
        new_grid = str(self._grid)
        if original_grid != new_grid: # if any tiles moved
            self.new_tile()
        
    
    def get_lines(self, direction): 
        '''
        grid -> lines
        
        When the direction is given, the list initial_tiles is also given (see __init__).
        Each initial tile (each item in initial_tiles) is the first tile of a line (a row or a column) 
        to be processed, so each initial tile indicates a line to be processed. 
        This helper function gets all these rows or columns.
        '''
        lines = [] # contains four lines to be processed by the merge function, each for one column (UP/DOWN) or one row (LEFT/RIGHT)
        start_cells = self._initial_tiles[direction]
        vector = OFFSETS[direction] 
        if direction == UP or direction == DOWN:
            num_steps = self.get_grid_height()
        elif direction == LEFT or direction == RIGHT:
            num_steps = self.get_grid_width()
        for start_cell in start_cells:
            this_line = []
            for step in range(num_steps):
                row = start_cell[0] + step * vector[0]
                col = start_cell[1] + step * vector[1]
                this_line.append(self._grid[row][col])
            lines.append(this_line)
        return lines
    
    
    def update_grid(self, direction, merged_lines):
        '''
        merged_lines -> grid
        '''
        start_cells = self._initial_tiles[direction]
        vector = OFFSETS[direction] 
        if direction == UP or direction == DOWN:
            num_steps = self.get_grid_height()
        elif direction == LEFT or direction == RIGHT:
            num_steps = self.get_grid_width()
        for idx1, start_cell in enumerate(start_cells):
            for idx2, step in enumerate(range(num_steps)):
                row = start_cell[0] + step * vector[0]
                col = start_cell[1] + step * vector[1]
                self._grid[row][col] = merged_lines[idx1][idx2]
            
            

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # decide which tile to choose
        empty_tiles = []
        for idx_row, row in enumerate(self._grid):
            for idx_col, col in enumerate(row):
                if col == 0:
                    empty_tiles.append((idx_row,idx_col))
        chosen_tile = random.sample(empty_tiles,1)
        chosen_tile = chosen_tile[0]
        
        # decide the figure for the new tile
        rand = random.random()
        if rand < 0.9:
            chosen_figure = 2
        else:
            chosen_figure = 4
            
        # print (chosen_tile, chosen_figure)
        
        # assign value for the tile
        self.set_tile(chosen_tile[0],chosen_tile[1],chosen_figure)
        
        
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value
        


    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

