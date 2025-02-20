from enum import Enum
from search import bfs, dfs, a_star, greedy_bfs, beam, GridState
import pygame

# Constants
SCREEN_SIZE = 1000
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
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip() 

    clock.tick(2)

pygame.quit()

#TODO: Build Grid
def grid(state : list[list[int]]):
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

#TODO: Build UI
