from enum import Enum
from search import bfs, dfs, a_star, greedy_bfs, beam, GridState, SearchManager
import pygame
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import ButtonArray

# TODO
# - handle clicks on squares
# - change grid state
# - implement search algos
# - add buttons (as  button array widget) for play, reset, and next step

# Constants
SCREEN_SIZE = 1000
GRID_SIZE = 10
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
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

def grid(state : list[list[GridState]]):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            match state[row][col]:
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
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid line
        # print grid state for debugging
        # for row in state:
        #     print(row)
        # print()

# Set up pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Interactable Pathfinding Visualizer")
running = True

# Set up search manager (manages grid and algorithms state)
searchManager = SearchManager()

# Set up UI
algo_dropdown = Dropdown(
    screen, 10, 10, 100, 50, name="Algorithms",
    choices=[algo.name for algo in Algorithm],
    values=[algo.value[1] for algo in Algorithm],
    borderRadius=5
)
edit_mode_dropdown = Dropdown(
    screen, 120, 10, 100, 50, name="Edit Mode",
    choices=[mode.name for mode in EditMode],
    values=[mode for mode in EditMode],
    borderRadius=5
)
simulation_control_buttons = ButtonArray(
    screen, 230, 10, 200, 50, (4,1), border=0,
    texts=('play', 'pause', 'next', 'reset'),
    onClicks=(
        lambda: print("TODO"),
        lambda: print("TODO"),
        lambda: print("TODO"),
        lambda: print("TODO")
    )
)

def pos_on_button(pos):
    dropdown_open = algo_dropdown.isDropped() or edit_mode_dropdown.isDropped()
    y_in_range = 10 <= pos[1] <= 60
    x_in_range = 10 <= pos[0] <= 110 or 120 <= pos[0] <= 220 or 230 <= pos[0] <= 430
    # print(f"dropdown open?: {dropdown_open}")
    # print(f"is Y in range? : {10 <= pos[1] <= 60}")
    # print(f"is X in range? : {10 <= pos[0] <= 110} or {120 <= pos[0] <= 220} or {230 <= pos[0] <= 430}")
    # print(f"are both in range?: {(10 <= pos[1] <= 60) and ((10 <= pos[0] <= 110) or (120 <= pos[0] <= 220) or (230 <= pos[0] <= 430))}")
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
                        if searchManager.grid[row][col] == GridState.UNEXPLORED:
                            searchManager.set_goal((row, col))
                    case EditMode.OBSTACLES:
                        print(searchManager.grid[row][col], searchManager.grid[row][col] == GridState.UNEXPLORED)
                        if searchManager.grid[row][col] == GridState.UNEXPLORED:
                            searchManager.grid[row][col] = GridState.OBSTACLE

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    grid(searchManager.grid)

    pygame_widgets.update(events)

    # flip() the display to put your work on screen
    pygame.display.update() 

    # clock.tick(2)

pygame.quit()