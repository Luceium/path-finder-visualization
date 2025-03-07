from enums import Algorithm, GridState, Cell
from collections import deque
import heapq
from collections.abc import Callable

class SearchManager:
    def __init__(self, _size=10, _beam_size=3):
        self.size = _size
        self.grid = [[Cell() for _ in range(self.size)] for _ in range(self.size)]

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
                self.a_star()
            case Algorithm.BEAM:
                self.beam(self.beam_size)
    
    def reset_grid(self):
        self.grid = [[Cell(self.grid[x][y].gridState) if self.grid[x][y].gridState != GridState.SEEN and self.grid[x][y].gridState != GridState.PATH else Cell() for y in range(self.size)] for x in range(self.size)]
        # reset the last seen (important if the goal was not reached)
        if self.last_explored:
            last_x, last_y = self.last_explored
            self.grid[last_x][last_y] = Cell()        
        # reset state of goal incase it was reached
        if self.goal_pos:
            goal_x, goal_y = self.goal_pos
            self.grid[goal_x][goal_y] = Cell(GridState.GOAL)
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
            self.grid[old_x][old_y].gridState = GridState.UNEXPLORED
        self.goal_pos = goal
        self.grid[goal[0]][goal[1]].gridState = GridState.GOAL

    def set_start(self, start: tuple[int, int]):
        # reset if anything has been explored
        if self.path_started:
            self.reset()
        if self.start_pos is not None:
            old_x, old_y = self.start_pos
            self.grid[old_x][old_y].gridState = GridState.UNEXPLORED
        self.start_pos = start
        self.grid[start[0]][start[1]].gridState = GridState.START
    
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

        self.add_neighbors(self.dfs_stack, lambda current: self.dfs_stack.append(current), self.dfs_handle_existing_neighbor)
    
    def dfs_handle_existing_neighbor(self, current):
        """
        Handles the case where a neighbor is already in the stack.
        Using recursion there is no stack data structure to remove
        the neighbor from so nodes can be seen as a next option but
        later be explored by a different node.

        In this case we'll move the neighbor to the end of the stack
        to ensure it is explored right away.
        """
        # remove the current node from the stack
        self.dfs_stack.remove(current)
        # add it to the end of the stack
        self.dfs_stack.append(current)
        # set the ancestor to the last explored node
        # this is important to ensure the path is correct
        x, y = current
        self.grid[x][y].ancestor = self.last_explored

    # Informed
    def a_star(self):
        """
        A*
        Searches based on the cost so far to a node + the heuristic cost estimate remaining.
        Combines the best of uninformed searches and informed searches.
        """
        # if not self.explore_next(self.a_star_queue, lambda: heapq.heappop(self.a_star_queue)[1]):
        #     return
        # distance = #TODO
        # self.add_neighbors(self.a_star_queue, lambda current: heapq.heappush(self.a_star_queue, (self.heuristic(current) + distance, current)))

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
                self.grid[x][y].gridState = GridState.SEEN

            # Color and set new current
            if len(data) < 1:
                return False# No solution found (May not be possible)
            self.last_explored = get_next()
            x, y = self.last_explored
            self.grid[x][y].gridState = GridState.CURRENT

            if self.last_explored == self.goal_pos:
                print("GOAL")
                self.colorPath()
                self.finished = True
                return False
        
        # If the user adds obstacles after a cell has been added to the
        # data structure for next options to explore we need to skip that node.
        x, y = self.last_explored
        if self.grid[x][y].gridState == GridState.OBSTACLE:
            return self.explore_next(data, get_next)
        
        return True
    
    def add_neighbors(self, next_options, add: Callable[[tuple[int,int]], None], handleExistingNeighbor: Callable[[tuple[int,int]], None]=lambda current: None):
        """
        Abstracts the consistent steps of checking all neighbors and adding them to a data structure.
        To be used in algorithms with vastly different search approaches, this function relies on callables to handle unique behavior.
        NOTE: this assumes all neighbors are explored. Algorithms like beam search don't operate this way.
        """
        x, y = self.last_explored

        for i,j in [(-1,0), (0,1), (1,0), (0,-1)]:
            current_x, current_y = x + i, y + j
            current = (current_x, current_y)

            if 0 <= current_x < self.size and 0 <= current_y < self.size and (self.grid[current_x][current_y].gridState == GridState.UNEXPLORED or self.grid[current_x][current_y].gridState == GridState.GOAL):
                # check if cell is in queue
                in_next = False
                for cell in next_options:
                    if cell == current:
                        in_next = True
                        break
                if not in_next:
                    add(current)
                    self.grid[current_x][current_y].ancestor = self.last_explored
                else:
                    handleExistingNeighbor(current)

    def search_impl(data, get_next: Callable[[], tuple[int,int]], add: Callable[[tuple[int,int]], None]):
        if not self.explore_next(data, get_next):
            return

        self.add_neighbors(data, add, self.last_explored)

    def colorPath(self):
        """
        Colors in all the cells visited in the path that got to the goal.
        """
        cell_pos = self.grid[self.last_explored[0]][self.last_explored[1]].ancestor

        while self.start_pos != cell_pos:
            x, y = cell_pos
            cell = self.grid[x][y]
            cell.gridState = GridState.PATH
            cell_pos = cell.ancestor

    def pathLength(self,pos):
        count = 0
        while pos != self.start_pos:
            count += 1
            pos = self.grid[pos[0]][pos[1]].ancestor
        return count

    def heuristic(self,pos):
        cur_x, cur_y = pos
        goal_x, goal_y = self.goal_pos
        return ((goal_x-cur_x)**2+(goal_y-cur_y)**2)**0.5


