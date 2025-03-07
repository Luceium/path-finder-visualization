from enum import Enum, auto

class GridState(Enum):
    START = auto()
    GOAL = auto()
    OBSTACLE = auto()
    UNEXPLORED = auto()
    SEEN = auto()
    CURRENT = auto()
    PATH = auto()

# UI Options
class EditMode(Enum):
    START = 'Edit Start'
    GOAL = 'Edit Goal'
    OBSTACLES = 'Edit Obstacles'

class Algorithm(Enum):
    #NOTE: Switching the algorithm resets the search
    BFS = "Breadth First Search"
    DFS = "Depth First Search"
    A_STAR = "A*"
    GREEDY_BFS = "Greedy Best First Search"
    BEAM = "Beam Search"

class Cell:
    def __init__(self, gridState=GridState.UNEXPLORED):
        self.gridState = gridState
        self.ancestor = None
        # self.pos Is this needed?
