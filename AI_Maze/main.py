import pygame
import sys
import random
from agent import QLearningAgent

# ====================================
# 1. CONFIGURATION & CONSTANTS
# ====================================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 40          # The world is divided into 40x40 pixel blocks
FPS = 2                # Game speed slowled down to watch de AI learn
HAZARD_LIFETIME = 50    # How many frames a hazard stays on screen
SPAWN_CHANCE = 0.10     #10% chance to spawn a new hazard every single frame

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

# Actions: 0=UP, 1=DOWN, 2=LEFT, 3-RIGHT
agent = QLearningAgent(actions=[0, 1, 2, 3])

def get_state(x, y, hazards_lists):
     """
     The AI's Radar. Looks 1 block for every direction.
     Returns a tuple of 4 values (0 for safe, 1 for danger)
     """
     danger_up = 1 if y - GRID_SIZE < 0 or (x, y - GRID_SIZE) in hazards_lists else 0
     danger_down = 1 if y + GRID_SIZE >= WINDOW_HEIGHT or (x, y + GRID_SIZE) in hazards_lists else 0
     danger_left = 1 if x - GRID_SIZE < 0 or (x - GRID_SIZE, y) in hazards_lists else 0
     danger_right = 1 if x + GRID_SIZE >= WINDOW_WIDTH or (x + GRID_SIZE, y) in hazards_lists else 0

     # States is a tuple like (1, 0, 0, 1) meaning danger UP and RIGHT
     return(danger_up, danger_down, danger_left, danger_right)


# Function to generate a new random maze
def generate_maze():
    new_hazards = {}
    
    # Loop through every possible column (X) and row (Y) in our grid
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
         for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
               
               # PROTECT THE SPAWN: Don't put a hazard where the player starts!
               if x == START_X and y == START_Y:
                    continue
               
               # 20% chance to spawn a hazard in the current block
               if random.random() < 0.20:
                    # Set the key (x, y) with a random initial lifetime value
                    new_hazards[(x, y)] = random.randint(20, HAZARD_LIFETIME)
    
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
    
    # --------------------------------------
    # B. GAME LOGIC UPDATE (THE AI BRAIN)
    # --------------------------------------
    
    # UPDATE DYNAMIC ENVIRONMENT
    # 1. Age exiting hazards and remove dead ones
    keys_to_remove = []
    for pos in hazards:
         hazards[pos] -= 1 # Decrease lifetime by 1 frame
         if hazards[pos] <= 0:
              keys_to_remove.append(pos)

    for pos in keys_to_remove:
         del hazards[pos] # Delete the hazard from dictionary

    # 2. Randomly spawn new hazards during gameplay
    if random.random() < SPAWN_CHANCE:
         # Pick a random grid coordinate
         hx = random.randrange(0, WINDOW_WIDTH, GRID_SIZE)
         hy = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)

         # Make sure ir doesn't spaws ON the player or where alrealdy exists
         if (hx, hy) != (player_x, player_y) and (hx, hy) not in hazards:
              hazards[(hx, hy)] = HAZARD_LIFETIME


    # KNOWLEDGE CICLE
    # 1. Observe the current state (Radar)
    current_state = get_state(player_x, player_y, hazards)

    # 2. Ask the Brain what to do
    action = agent.choose__action(current_state)

    # 3. Predict where the action will take us
    next_x, next_y = player_x, player_y
    if action == 0: next_y -= GRID_SIZE     # UP
    elif action == 1: next_y += GRID_SIZE   # DOWN
    elif action == 2: next_x -= GRID_SIZE   # LEFT
    elif action == 3: next_y += GRID_SIZE   # RIGHT

    # 4. Check if the planned move is deadly (wall or red bloack)
    is_deadly = False
    if next_x < 0 or next_x >= WINDOW_WIDTH or next_y < 0 or next_y >= WINDOW_HEIGHT:
         is_deadly = True # Hit a boundary wall
    elif (next_x, next_y) in hazards:
         is_deadly = True # Hit a red hazard

    # 5. Assing Rewards and Move
    if is_deadly:
         reward = -100
         print(f"Crash AI Randomness (Epsilon): {agent.epsilon:.2f} | Resetting map...")
         player_x = START_X
         player_y = START_Y
         hazards = generate_maze() # Rebuild de world on death

    else:
         reward = 1 # Survived this step!
         player_x, player_y = next_x, next_y # Actually move the character

    # 6. Observe the new state after moving
    next_state = get_state(player_x, player_y, hazards)

    # 7. TEACH THE BRAIN (Update the Q-Table)
    agent.learn(current_state, action, reward, next_state)

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