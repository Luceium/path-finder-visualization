from enums import Algorithm, GridState
from collections import deque
import heapq
from collections.abc import Callable

class SearchManager:
    def __init__(self, _size=10, _beam_size=3):
        self.size = _size
        self.grid = [[GridState.UNEXPLORED for _ in range(self.size)] for _ in range(self.size)]

        # BFS
        self.bfs_queue = deque()
        # DFS
        self.dfs_stack = []
        # A*
        self.a_star_queue = []
        heapq.heapify(self.a_star_queue)
        # Greedy BFS
        self.greedy_bfs_queue = []
        heapq.heapify(self.greedy_bfs_queue)
        # Beam
        self.beam_size = _beam_size
        self.beam_queue = []
        heapq.heapify(self.beam_queue)

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
                self.dfs()
            case Algorithm.GREEDY_BFS:
                self.greedy_bfs()
            case Algorithm.A_STAR:
                pass
            case Algorithm.BEAM:
                pass
    
    def reset_grid(self):
        self.grid = [[self.grid[x][y] if self.grid[x][y] != GridState.SEEN else GridState.UNEXPLORED for y in range(self.size)] for x in range(self.size)]
        # reset the last seen (important if the goal was not reached)
        last_x, last_y = self.last_explored
        self.grid[last_x][last_y] = GridState.UNEXPLORED        
        # reset state of goal incase it was reached
        goal_x, goal_y = self.goal_pos
        self.grid[goal_x][goal_y] = GridState.GOAL
        # NOTE: If the last explored was the goal, the goal will still be properly colored
        # because we set the goal after

    def reset(self):
        # reset all state vars
        self.reset_grid()
        self.path_started = False
        self.last_explored = None
        self.finished = False
        self.bfs_queue = deque()
        self.greedy_bfs_queue = []
        heapq.heapify(self.greedy_bfs_queue)
        self.dfs_stack = []
        self.a_star_queue = []
        heapq.heapify(self.a_star_queue)
        self.beam_queue = []
        heapq.heapify(self.beam_queue)


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
        if not self.explore_next(self.bfs_queue, lambda: self.bfs_queue.popleft()):
            return

        self.add_neighbors(self.bfs_queue, lambda current: self.bfs_queue.append(current))

    def dfs(self):
        """
        Depth First Search
        Searches one path at a time, completely exploring a path and all it's subpaths before moving on to a new path.
        """
        #Note - path seems a bit buggy
        if not self.explore_next(self.dfs_stack, lambda: self.dfs_stack.pop()):
            return

        self.add_neighbors(self.dfs_stack, lambda current: self.dfs_stack.append(current))

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
        if not self.explore_next(self.greedy_bfs_queue, lambda: heapq.heappop(self.greedy_bfs_queue)[1]):
            return
        
        self.add_neighbors(self.greedy_bfs_queue, lambda current: heapq.heappush(self.greedy_bfs_queue, (self.heuristic(current), current)))

    def beam(self, n):
        """
        Beam Search
        Explores the top n nodes at each step of the search and prunes all other nodes.
        """
        return 5

    # Algo Helper Functions
    def explore_next(self, data, get_next: Callable[[], tuple[int,int]]) -> bool:
        if self.finished:
            return False
        if not self.path_started: # Start
            self.last_explored = self.start_pos
            self.path_started = True
        else:
            # Unset last seen
            if self.last_explored != self.start_pos:
                x, y = self.last_explored
                self.grid[x][y] = GridState.SEEN

            # Color and set new current
            if len(data) < 1:
                return False# No solution found (May not be possible)
            self.last_explored = get_next()
            x, y = self.last_explored
            self.grid[x][y] = GridState.CURRENT

            if self.last_explored == self.goal_pos:
                print("GOAL")
                self.finished = True
                return False
        
        # If the user adds obstacles after a cell has been added to the
        # data structure for next options to explore we need to skip that node.
        x, y = self.last_explored
        if self.grid[x][y] == GridState.OBSTACLE:
            return self.explore_next(data, get_next)
        
        return True
    
    def add_neighbors(self, next_options, add: Callable[[tuple[int,int]], None]):
        x, y = self.last_explored

        for i,j in [(-1,0), (0,1), (1,0), (0,-1)]:
            current_x, current_y = x + i, y + j
            current = (current_x, current_y)

            if 0 <= current_x < self.size and 0 <= current_y < self.size and (self.grid[current_x][current_y] == GridState.UNEXPLORED or self.grid[current_x][current_y] == GridState.GOAL):
                # check if cell is in queue
                in_next = False
                for cell in next_options:
                    if cell == current:
                        in_next = True
                        break
                if not in_next:
                    add(current)

    def heuristic(self,pos):
        cur_x, cur_y = pos
        goal_x, goal_y = self.goal_pos
        return ((goal_x-cur_x)**2+(goal_y-cur_y)**2)**0.5


