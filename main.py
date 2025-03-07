from search import SearchManager
from enums import GridState, EditMode, Algorithm, Cell
import pygame
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import ButtonArray
import threading
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Constants
SCREEN_SIZE = 1005
GRID_SIZE = 15 # NOTE: If you change this, any existing maze won't work
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
WHITE = (255, 255, 255) # unvisited
BLACK = (0, 0, 0)       # obstacles
GREEN = (0, 255, 0)     # start
YELLOW = (255, 255, 0)  # goal
GREY = (169, 169, 169)  # explored
BLUE = (0, 0, 255)      # last visited cell
PATH = (255, 0, 0)      # Color for path to goal
MAZE_FILE_PATH = "maze.csv"

# Save and load functions
def save_maze(grid_state):
    with open(MAZE_FILE_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in grid_state:
            # Convert enum to int values for storage
            writer.writerow([cell.gridState.value for cell in row])
    print(f"Maze saved to {MAZE_FILE_PATH}")

def load_maze():
    if not os.path.exists(MAZE_FILE_PATH):
        return None
    
    try:
        with open(MAZE_FILE_PATH, 'r', newline='') as f:
            reader = csv.reader(f)
            grid = []
            for row in reader:
                if not row:
                    continue
                grid_row = []
                for cell in row:
                    # Convert back from int to GridState enum
                    grid_row.append(GridState(int(cell)))
                grid.append(grid_row)
            
            # Validate grid dimensions
            if len(grid) == GRID_SIZE and all(len(row) == GRID_SIZE for row in grid):
                print(f"Maze loaded from {MAZE_FILE_PATH}")
                return grid
    except Exception as e:
        print(f"Error loading maze: {e}")
    
    return None

def grid(state : list[list[Cell]]):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            match state[row][col].gridState:
                case GridState.UNEXPLORED:
                    pygame.draw.rect(screen, WHITE, rect)
                case GridState.SEEN:
                    pygame.draw.rect(screen, GREY, rect)
                case GridState.OBSTACLE:
                    pygame.draw.rect(screen, BLACK, rect)
                case GridState.START:
                    pygame.draw.rect(screen, GREEN, rect)
                case GridState.GOAL:
                    pygame.draw.rect(screen, YELLOW, rect)
                case GridState.CURRENT:
                    pygame.draw.rect(screen, BLUE, rect)
                case GridState.PATH:
                    pygame.draw.rect(screen, PATH, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid line
        # print grid state for debugging
        # for row in state:
        #     print(row)
        # print()search

# Set up pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Interactable Pathfinding Visualizer")
running = True

# Set up search manager (manages grid and algorithms state)
searchManager = SearchManager(_size=GRID_SIZE)

# Try to load maze from file
saved_grid = load_maze()
if saved_grid:
    # Convert the loaded grid states to Cell objects
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            searchManager.grid[r][c] = Cell(saved_grid[r][c])
            # Find start and goal positions
            if saved_grid[r][c] == GridState.START:
                searchManager.set_start((r, c))
            elif saved_grid[r][c] == GridState.GOAL:
                searchManager.set_goal((r, c))

algo_dropdown = Dropdown(
    screen, 10, 10, 100, 50, name="Algorithms",
    choices=[algo.value for algo in Algorithm],
    values=[algo for algo in Algorithm],
    borderRadius=5
)
edit_mode_dropdown = Dropdown(
    screen, 120, 10, 100, 50, name="Edit Mode",
    choices=[mode.name for mode in EditMode],
    values=[mode for mode in EditMode],
    borderRadius=5
)

play_thread = None
pause_event = threading.Event()
end_event = threading.Event()

def play_search():
    global play_thread
    if play_thread is None or not play_thread.is_alive():
        end_event.clear()
        pause_event.clear()
        play_thread = threading.Thread(target=run_search)
        play_thread.start()

def run_search():
    while not end_event.is_set() and not searchManager.finished:
        if not pause_event.is_set():
            searchManager.search(algo_dropdown.getSelected())
            pygame.time.wait(250)

def toggle_pause():
    if pause_event.is_set():
        pause_event.clear()
    else:
        pause_event.set()

def reset():
    global play_thread
    if play_thread is not None:
        end_event.set()
        play_thread.join()
        play_thread = None
    searchManager.reset()

def run_analysis():
    """
    Run all algorithms and compare their performance.
    Captures the number of cells visited and path length for each algorithm.
    """
    algorithms = [Algorithm.BFS, Algorithm.DFS, Algorithm.GREEDY_BFS, Algorithm.A_STAR]
    results = []
     
    for algo in algorithms:
        searchManager.reset()
        
        # Run algorithm and collect results
        result = searchManager.run_algorithm_to_completion(algo)
        results.append(result)
        print(f"{algo.value}: Visited {result['cells_visited']} cells, Path length: {result['path_length']}")
    
    visualize_results(results)

def visualize_results(results):
    """
    Create a matplotlib visualization of algorithm performance
    """
    # Extract data for plotting
    algorithm_names = [result['algorithm'] for result in results]
    cells_visited = [result['cells_visited'] for result in results]
    path_lengths = [result['path_length'] for result in results]
    
    # Create bar chart
    x = np.arange(len(algorithm_names))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12,8))
    rects1 = ax.bar(x - width/2, cells_visited, width, label='Cells Visited')
    rects2 = ax.bar(x + width/2, path_lengths, width, label='Path Length')
    
    # Add labels and formatting
    ax.set_title('Algorithm Performance Comparison')
    ax.set_xlabel('Algorithm')
    ax.set_ylabel('Count')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithm_names)
    ax.legend()
    
    # Add data labels on bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    # Display the plot
    plt.tight_layout()
    plt.savefig('algorithm_analysis.png')
    plt.show()

simulation_control_buttons = ButtonArray(
    screen, 230, 10, 300, 50, (6,1), border=0,
    texts=('play', 'pause', 'next', 'reset', 'save', 'analyze'),
    onClicks=(
        lambda: play_search(),
        lambda: toggle_pause(),
        lambda: searchManager.search(algo_dropdown.getSelected()),
        lambda: reset(),
        lambda: save_maze(searchManager.grid),
        lambda: run_analysis()
    )
)

def pos_on_button(pos):
    dropdown_open = algo_dropdown.isDropped() or edit_mode_dropdown.isDropped()
    y_in_range = 10 <= pos[1] <= 60
    x_in_range = 10 <= pos[0] <= 110 or 120 <= pos[0] <= 220 or 230 <= pos[0] <= 530
    return dropdown_open or (y_in_range and x_in_range)

while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if not pos_on_button(pos):
                row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                edit_choice = edit_mode_dropdown.getSelected()
                match edit_choice:
                    case EditMode.START:
                        searchManager.set_start((row, col))
                    case EditMode.GOAL:
                        if searchManager.grid[row][col].gridState == GridState.UNEXPLORED:
                            searchManager.set_goal((row, col))
                    case EditMode.OBSTACLES:
                        if searchManager.grid[row][col].gridState == GridState.UNEXPLORED:
                            searchManager.grid[row][col].gridState = GridState.OBSTACLE
                        elif searchManager.grid[row][col].gridState == GridState.OBSTACLE:
                            searchManager.grid[row][col].gridState = GridState.UNEXPLORED

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    grid(searchManager.grid)

    pygame_widgets.update(events)

    # flip() the display to put your work on screen
    pygame.display.update() 

    # clock.tick(2)

pygame.quit()