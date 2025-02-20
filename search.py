from enum import Enum, auto

# ALGO IMPLEMENTATIONS
# NOTE: All functions will perform 1 step (explore one unit) to make the program intractable

# Uninformed
def bfs():
    """
    Breadth First Search
    Searches all paths at the same time, expanding each equally.
    """
    return 1

def dfs():
    """
    Depth First Search
    Searches one path at a time, completely exploring a path and all it's subpaths before moving on to a new path.
    """
    return 2

# Informed
def a_star():
    """
    A*
    Searches based on the cost so far to a node + the heuristic cost estimate remaining.
    Combines the best of uninformed searches and informed searches.
    """
    return 3

def greedy_bfs():
    """
    Greedy Best First Search
    Greedily searches based on which node has the smallest heuristic cost to the goal.
    """
    return 4

def beam(n):
    """
    Beam Search
    Explores the top n nodes at each step of the search and prunes all other nodes.
    """
    return 5


class GridState(Enum):
    START = auto()
    GOAL = auto()
    OBSTACLE = auto()
    UNEXPLORED = auto()
    SEEN = auto()
    CURRENT = auto()

class SearchManager:
    def __init__(self, _defaultImpl=bfs, _size=10, _beam_size=3):
        self.impl = _defaultImpl
        self.size = _size
        self.grid = [[GridState.UNEXPLORED for _ in range(self.size)] for _ in range(self.size)]

        # BFS
        bfs_queue = []
        # DFS
        dfs_stack = []
        # A*
        a_star_queue = []
        # Greedy BFS
        greedy_bfs_queue = []
        # Beam
        beam_size = _beam_size
    
    def reset_grid(self):
        self.grid = [[GridState.UNEXPLORED for _ in range(self.size)] for _ in range(self.size)]

    def step(self):
        if self.impl == beam:
            self.impl(self.beam_size)
        else:
            self.impl()

    def reset(self):
        # reset all state vars
        pass
    
    def changeImpl(self, newImpl):
        self.impl = newImpl
