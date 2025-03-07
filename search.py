"""
Search Algorithm Implementation Module

This module contains implementations of various pathfinding algorithms:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Greedy Best-First Search
- A* Search
- Beam Search

Each algorithm is implemented to work step-by-step for visualization purposes.
"""
from enums import Algorithm, GridState, Cell
from collections import deque
import heapq
from collections.abc import Callable

class SearchManager:
    """
    Manages grid state and pathfinding algorithm execution.
    
    This class handles the grid representation, algorithm selection and execution,
    and maintains state for visualization purposes. It supports step-by-step
    execution of algorithms to enable visual demonstration of how each algorithm works.
    
    Attributes:
        size (int): The size of the grid (size x size).
        grid (list): 2D grid of Cell objects representing the search space.
        bfs_queue (deque): Queue used for BFS algorithm.
        dfs_stack (list): Stack used for DFS algorithm.
        a_star_queue (list): Priority queue used for A* algorithm.
        greedy_bfs_queue (list): Priority queue used for Greedy BFS algorithm.
        beam_size (int): Maximum number of paths to explore in Beam Search.
        beam_queue (list): Priority queue used for Beam Search algorithm.
        goal_pos (tuple): (x, y) coordinates of the goal position.
        start_pos (tuple): (x, y) coordinates of the start position.
        path_started (bool): Flag indicating if search has started.
        last_explored (tuple): (x, y) coordinates of the last explored cell.
        finished (bool): Flag indicating if search has finished.
        cells_visited (int): Counter for number of cells visited during search.
    """
    def __init__(self, _size=10, _beam_size=3):
        """
        Initialize the SearchManager with a grid and algorithm data structures.
        
        Args:
            _size (int): Size of the grid (creates a _size x _size grid).
            _beam_size (int): Number of paths to keep for beam search.
        """
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
        self.cells_visited = 0

    def search(self, algo: Algorithm):
        """
        Execute one step of the selected search algorithm.
        
        Args:
            algo (Algorithm): The algorithm to use for search.
        """
        match algo:
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
        """
        Reset the grid to its initial state while preserving obstacles, start, and goal.
        
        This method clears all search-related cell states (SEEN, PATH) but preserves the
        obstacles, start, and goal positions.
        """
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
        """
        Reset all search state variables and clear the grid visualization.
        
        Resets all algorithm data structures, path visualization, and counters
        while preserving the maze layout.
        """
        # reset all state vars
        self.reset_grid()
        self.path_started = False
        self.last_explored = None
        self.finished = False
        self.cells_visited = 0
        self.bfs_queue = deque()
        self.greedy_bfs_queue = []
        heapq.heapify(self.greedy_bfs_queue)
        self.dfs_stack = []
        self.a_star_queue = []
        heapq.heapify(self.a_star_queue)
        self.beam_queue = []
        heapq.heapify(self.beam_queue)


    def set_goal(self, goal: tuple[int, int]):
        """
        Set the goal position on the grid.
        
        Args:
            goal (tuple): (x, y) coordinates for the goal position.
        """
        if self.goal_pos is not None:
            old_x, old_y = self.goal_pos
            self.grid[old_x][old_y].gridState = GridState.UNEXPLORED
        self.goal_pos = goal
        self.grid[goal[0]][goal[1]].gridState = GridState.GOAL

    def set_start(self, start: tuple[int, int]):
        """
        Set the start position on the grid.
        
        If a search is already in progress, it resets the search first.
        
        Args:
            start (tuple): (x, y) coordinates for the start position.
        """
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
        Breadth-First Search algorithm implementation.
        
        Searches all paths at the same time, expanding each path equally one step at a time.
        This ensures the shortest path (in terms of steps) is found.
        """
        self.search_impl(
            self.bfs_queue,
            lambda: self.bfs_queue.popleft(),
            lambda current: self.bfs_queue.append(current)
        )

    def dfs(self):
        """
        Depth-First Search algorithm implementation.
        
        Explores one path fully before backtracking to explore alternate paths.
        May not find the shortest path, but can be more memory efficient than BFS.
        """
        self.search_impl(
            self.dfs_stack,
            lambda: self.dfs_stack.pop(),
            lambda current: self.dfs_stack.append(current),
            self.dfs_handle_existing_neighbor
        )
    
    def dfs_handle_existing_neighbor(self, current):
        """
        Special handler for DFS to manage neighbors already in the stack.
        
        When DFS encounters a neighbor already in the stack, this method ensures
        the path consistency by updating the ancestor relationship.
        
        Args:
            current (tuple): (x, y) coordinates of the neighbor cell.
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
        A* Search algorithm implementation.
        
        Combines path cost so far (like BFS) with a heuristic estimate of remaining
        cost to the goal. This generally finds the optimal path while exploring fewer
        nodes than BFS.
        """
        self.search_impl(
            self.a_star_queue,
            lambda: heapq.heappop(self.a_star_queue)[1],
            lambda current: heapq.heappush(self.a_star_queue, (self.heuristic(current) + self.pathLength(self.last_explored), current))
        )
        
    def greedy_bfs(self):
        """
        Greedy Best-First Search algorithm implementation.
        
        Prioritizes paths that appear to be closest to the goal according to a heuristic.
        Fast but may not find the optimal path.
        """
        self.search_impl(
            self.greedy_bfs_queue,
            lambda: heapq.heappop(self.greedy_bfs_queue)[1],
            lambda current: heapq.heappush(self.greedy_bfs_queue, (self.heuristic(current), current))
        )

    def beam(self, n):
        """
        Beam Search algorithm implementation.
        
        Similar to breadth-first search but only keeps the best n paths at each step.
        This limits memory usage but may miss the optimal solution.
        
        Args:
            n (int): The beam width - number of paths to maintain at each step.
        """
        pass

    # Algo Helper Functions
    def explore_next(self, data, get_next: Callable[[], tuple[int,int]]) -> bool:
        """
        Helper function for exploring the next cell in a search algorithm.
        
        Handles common operations like updating the last explored cell, checking for
        the goal, and advancing the search state.
        
        Args:
            data: The data structure containing cells to explore (queue, stack, etc.)
            get_next: Function that returns the next cell to explore from the data structure.
            
        Returns:
            bool: True if search should continue, False if search is complete or impossible.
        """
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
                return False # No solution found (May not be possible)
            self.last_explored = get_next()
            x, y = self.last_explored
            self.grid[x][y].gridState = GridState.CURRENT
            self.cells_visited += 1

            if self.last_explored == self.goal_pos:
                print(f"GOAL REACHED! Cells visited: {self.cells_visited}")
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
        Add valid neighboring cells to the search data structure.
        
        Checks the four adjacent cells (up, right, down, left) and adds valid ones
        to the data structure for future exploration.
        NOTE: This assumes all neighbors are explored. Algorithms like beam search only search beam_size many neighbors.

        Args:
            next_options: Data structure containing cells to explore.
            add: Function to add a cell to the data structure.
            handleExistingNeighbor: Optional function to handle neighbors already in the data structure.
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

    def search_impl(self, data, get_next: Callable[[], tuple[int,int]], add: Callable[[tuple[int,int]], None], handleExistingNeighbor: Callable[[tuple[int,int]], None]=lambda current: None):
        """
        Generic search implementation that can be configured for different algorithms.
        
        This is the core search function used by all the algorithms. It's customized
        through function parameters to implement specific search behaviors.
        
        Args:
            data: The data structure to use (queue, stack, heap, etc.)
            get_next: Function to get the next cell from the data structure.
            add: Function to add a cell to the data structure.
            handleExistingNeighbor: Function to handle neighbors already in data structure.
        """
        if not self.explore_next(data, get_next):
            return

        self.add_neighbors(data, add, handleExistingNeighbor)

    def colorPath(self):
        """
        Highlight the path from start to goal once goal is reached.
        
        Traces back from the goal to the start using ancestor pointers and
        updates the cell state to PATH for visualization.
        """
        cell_pos = self.grid[self.last_explored[0]][self.last_explored[1]].ancestor

        while self.start_pos != cell_pos:
            x, y = cell_pos
            cell = self.grid[x][y]
            cell.gridState = GridState.PATH
            cell_pos = cell.ancestor

    def pathLength(self, pos):
        """
        Calculate the path length from the start to the given position.
        
        Args:
            pos (tuple): (x, y) coordinates of the end position.
            
        Returns:
            int: The number of steps in the path.
        """
        count = 0
        while pos != self.start_pos:
            count += 1
            pos = self.grid[pos[0]][pos[1]].ancestor
        return count

    def heuristic(self, pos):
        """
        Calculate a heuristic estimate of distance from position to goal.
        
        Uses Euclidean distance as the heuristic function.
        
        Args:
            pos (tuple): (x, y) coordinates of the position.
            
        Returns:
            float: The estimated distance to the goal.
        """
        cur_x, cur_y = pos
        goal_x, goal_y = self.goal_pos
        return ((goal_x-cur_x)**2+(goal_y-cur_y)**2)**0.5

    def run_algorithm_to_completion(self, algo: Algorithm):
        """
        Run a search algorithm until it reaches the goal or exhausts all options.
        
        Used for analysis to compare performance metrics of different algorithms.
        
        Args:
            algo (Algorithm): The algorithm to run.
            
        Returns:
            dict: Performance metrics including cells visited and path length.
        """
        # Reset everything first
        self.reset()
        
        # Keep searching until finished or no more cells to explore
        steps = 0
        max_steps = self.size ** 2 * 2  # Avoid infinite loops
        
        while not self.finished and steps < max_steps:
            self.search(algo)
            steps += 1
            
            # If no progress can be made (no more cells to explore)
            if steps > 0 and not self.path_started:
                break
        
        # Return the metrics
        path_length = 0
        if self.finished:
            path_length = self.pathLength(self.goal_pos)
            
        return {
            "algorithm": algo.value,
            "cells_visited": self.cells_visited,
            "path_length": path_length,
            "goal_reached": self.finished
        }


