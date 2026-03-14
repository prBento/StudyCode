import pygame
import sys
import random

# ====================================
# 1. CONFIGURATION & CONSTANTS
# ====================================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 40 # The world is divided into 40x40 pixel blocks
FPS = 30

# RGB Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)    # Agent
RED = (255, 0, 0)       # Hazard/Perigo

# ==========================================
# 2. SYSTEM INITIALIZATION
# ==========================================
# Initializes all imported pygame modules
pygame.init()

# Creates the game window and sets the title
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hybrid AI Maze")

# Creates an object to help track time and frame rate
clock = pygame.time.Clock()

# ==========================================
# 3. GAME STATE (VARIABLES)
# ==========================================
# We define start constants so we can easily reset the player later
START_X = 0
START_Y = 0
player_x = START_X
player_y = START_Y

# Function to generate a new random maze
def generate_maze():
    new_hazards = []
    
    # Loop through every possible column (X) and row (Y) in our grid
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
         for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
               # PROTECT THE SPAWN: Don't put a hazard where the player starts!
               if x == START_X and y == START_Y:
                    continue
               
               # 20% chance to spawn a hazard in the current block
               if random.random() < 0.20:
                    new_hazards.append((x,y))
    
    return new_hazards

# Create the first maze when the game starts
hazards = generate_maze()

# ==========================================
# 4. MAIN GAME LOOP
# ==========================================
# This loop keeps the game running until 'running' becomes False

running = True
while running:

    # --------------------------------------
    # A. EVENT HANDLING (INPUTS)
    # --------------------------------------
    # pygame.event.get() empties the event queue (clicks, key presses, etc.)
    for event in pygame.event.get():

        # if the user click the "X" button on the window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Grid-based movement logic with boundary checking to keep player on screen
            if event.key == pygame.K_UP:
                if player_y > 0:
                    player_y -= GRID_SIZE
            elif event.key == pygame.K_DOWN:
                    if player_y < WINDOW_HEIGHT - GRID_SIZE:
                        player_y += GRID_SIZE
            elif event.key == pygame.K_LEFT:
                    if player_x > 0:
                        player_x -= GRID_SIZE
            elif event.key == pygame.K_RIGHT:
                    if player_x < WINDOW_WIDTH - GRID_SIZE:
                        player_x += GRID_SIZE
    
    # --------------------------------------
    # B. GAME LOGIC UPDATE
    # --------------------------------------
    # Create a tuple of the player's current position
    player_pos = (player_x, player_y)

    # Check if the player stepped on any hazard
    if player_pos in hazards:
         print("Game Over! Restarting...")  # Prints to the VS Code terminal
         player_x = START_X                 # Reset X
         player_y = START_Y                 # Reset Y
         hazards = generate_maze()

    # --------------------------------------
    # C. RENDERING (DRAWING TO SCREEN)
    # --------------------------------------
    # 1. Clear the screen from the previous frame
    screen.fill(BLACK)

    # Draw all hazards using a loop
    for h_x, h_y in hazards:
         hazard_rect = (h_x, h_y, GRID_SIZE, GRID_SIZE)
         pygame.draw.rect(screen, RED, hazard_rect)

    # 2. Define de player's shape and position (X, Y, Width, Height)
    player_rect = (player_x, player_y, GRID_SIZE, GRID_SIZE)

    # 3. Draw the player rectangle onto the screen surface
    pygame.draw.rect(screen, BLUE, player_rect)

    # 4. Swap the memory buffer with the display (makes drawings visible)
    pygame.display.flip()

    # 5. Cap the frame rate to ensure consistent speed across different computers
    clock.tick(FPS)

# ==========================================
# 5. GRACEFUL EXIT
# ==========================================
# Uninitialize all pygame modules and close the script properly
pygame.quit()
sys.exit()