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
        self.bfs_queue = []
        # DFS
        self.dfs_stack = []
        # A*
        self.a_star_queue = []
        # Greedy BFS
        self.greedy_bfs_queue = []
        # Beam
        self.beam_size = _beam_size

        self.goal_pos = None
        self.start_pos = None
        self.path_started = False
    
    def reset_grid(self):
        self.grid = [[GridState.UNEXPLORED for _ in range(self.size)] for _ in range(self.size)]

    def step(self):
        if self.impl == beam:
            self.impl(self.beam_size)
        else:
            self.impl()

    def reset(self):
        # reset all state vars
        self.reset_grid()
        self.path_started = False

    def set_goal(self, goal: tuple[int, int]):
        if self.goal_pos is not None:
            old_x, old_y = self.goal_pos
            self.grid[old_x][old_y] = GridState.UNEXPLORED
        self.goal_pos = goal
        self.grid[goal[0]][goal[1]] = GridState.GOAL

    def set_start(self, start: tuple[int, int]):
        # reset if anything has been explored
        if self.path_started:
            self.reset()
        if self.start_pos is not None:
            old_x, old_y = self.start_pos
            self.grid[old_x][old_y] = GridState.UNEXPLORED
        self.start_pos = start
        self.grid[start[0]][start[1]] = GridState.START
    
    def changeImpl(self, newImpl):
        self.impl = newImpl
