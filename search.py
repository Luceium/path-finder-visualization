from enums import Algorithm, GridState
from collections import deque

class SearchManager:
    def __init__(self, _size=10, _beam_size=3):
        self.size = _size
        self.grid = [[GridState.UNEXPLORED for _ in range(self.size)] for _ in range(self.size)]

        # BFS
        self.bfs_queue = deque()
        # DFS
        self.dfs_stack = []
        # A*
        self.a_star_queue = deque()
        # Greedy BFS
        self.greedy_bfs_queue = deque()
        # Beam
        self.beam_size = _beam_size
        self.beam_queue = deque()

        self.goal_pos = None
        self.start_pos = None
        self.path_started = False
        self.last_explored = None
        self.finished = False

    def search(self, impl: Algorithm):
        match impl:
            case Algorithm.BFS:
                self.bfs()
            case Algorithm.DFS:
                pass
            case Algorithm.GREEDY_BFS:
                pass
            case Algorithm.A_STAR:
                pass
            case Algorithm.BEAM:
                pass
    
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
        self.goal_pos = None
        self.start_pos = None
        self.path_started = False
        self.last_explored = None
        self.finished = False
        self.bfs_queue = deque()
        self.greedy_bfs = deque()
        self.dfs_stack = []
        self.a_star_queue = deque()
        self.beam_queue = deque()


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
    
    # ALGO IMPLEMENTATIONS
    # NOTE: All functions will perform 1 step (explore one unit) to make the program intractable

    # Uninformed
    def bfs(self):
        """
        Breadth First Search
        Searches all paths at the same time, expanding each equally.
        """
        if self.finished:
            return
        if not self.path_started: # Start
            self.last_explored = self.start_pos
            self.path_started = True
        else:
            # Unset last seen
            if self.last_explored != self.start_pos:
                x, y = self.last_explored
                self.grid[x][y] = GridState.SEEN

            # Color and set new current
            if len(self.bfs_queue) < 1:
                return # No solution found (May not be possible)
            self.last_explored = self.bfs_queue.popleft()
            x, y = self.last_explored
            self.grid[x][y] = GridState.CURRENT

            print(self.last_explored, self.goal_pos)
            if self.last_explored == self.goal_pos:
                print("GOAL")
                self.finished = True

        x, y = self.last_explored

        for i,j in [(-1,0), (0,1), (1,0), (0,-1)]:
            current_x, current_y = x + i, y + j
            current = (current_x, current_y)

            if 0 <= current_x < self.size and 0 <= current_y < self.size and (self.grid[current_x][current_y] == GridState.UNEXPLORED or self.grid[current_x][current_y] == GridState.GOAL):
                # check if cell is in queue
                in_queue = False
                for cell in self.bfs_queue:
                    if cell == current:
                        in_queue = True
                        break
                if not in_queue:
                    self.bfs_queue.append(current)

    def dfs(self):
        """
        Depth First Search
        Searches one path at a time, completely exploring a path and all it's subpaths before moving on to a new path.
        """
        return 2

    # Informed
    def a_star(self):
        """
        A*
        Searches based on the cost so far to a node + the heuristic cost estimate remaining.
        Combines the best of uninformed searches and informed searches.
        """
        return 3

    def greedy_bfs(self):
        """
        Greedy Best First Search
        Greedily searches based on which node has the smallest heuristic cost to the goal.
        """
        return 4

    def beam(self, n):
        """
        Beam Search
        Explores the top n nodes at each step of the search and prunes all other nodes.
        """
        return 5

