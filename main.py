from enum import Enum

# Constants
SCREEN_SIZE = 10000
GRID_SIZE = 10
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
FPS = 30
WHITE = (255, 255, 255) # unvisited
BLACK = (0, 0, 0)       # obstacles
GREEN = (0, 255, 0)     # start
YELLOW = (255, 255, 0)  # goal
GREY = (169, 169, 169)  # explored
BLUE = (0, 0, 255)      # last visited cell

# UI options
class EditMode(Enum):
    START = 'Edit Start'
    GOAL = 'Edit Goal'
    OBSTACLES = 'Edit Obstacles'

class Algorithm(Enum):
    #NOTE: Switching the algorithm resets the search
    BFS = ("Breadth First Search", bfs)
    DFS = ("Depth First Search", dfs)
    A_STAR = ("A*", a_star)
    GREEDY_BFS = ("Greedy Best First Search", greedy_bfs)
    BEAM = ("Beam Search", beam)



# Path Finding Visualizer

#TODO: Set up pygame
#TODO: Build Grid
#TODO: Build UI
