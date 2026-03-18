import pygame
import sys
import random
import textwrap
import math
from agent import QLearningAgent
from director import GameDirector

# ====================================
# 1. CONFIGURATION & CONSTANTS
# ====================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAZE_WIDTH = WINDOW_WIDTH
GRID_SIZE = 40          # The world is divided into 40x40 pixel blocks
FPS = 2                 # Game speed slowed down to watch the AI learn

# RGB Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 100, 255)    # Agent
RED = (200, 50, 50)     # Hazard
DARK_GREY = (30, 30, 30)

# Convert frames into clock's time (MM:SS)
def format_time(frames):
     total_seconds = frames // FPS
     minutes = total_seconds // 60
     seconds = total_seconds % 60
     return f"{minutes:02d}:{seconds:02d}"

# ==========================================
# 2. SYSTEM INITIALIZATION
# ==========================================
# Initializes all imported pygame modules
pygame.init()

# Creates the game window and sets the title
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hybrid AI Maze")

# Creates an object to help track time and frame rate
clock = pygame.time.Clock()

font_main = pygame.font.SysFont('Consolas', 18, bold=True)
font_small = pygame.font.SysFont('Consolas', 15)

# ==========================================
# 3. GAME STATE (VARIABLES)
# ==========================================
# We define start constants so we can easily reset the player later
player_x = random.randrange(0, MAZE_WIDTH, GRID_SIZE)
player_y = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)

# Actions: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
agent = QLearningAgent(actions=[0, 1, 2, 3])

# AI Game Director & Metrics
director = GameDirector()

# Mutable environment variables (controlled by the LLM)
current_spawn_chance = 0.10
current_hazard_lifetime = 50
current_llm_reasoning = "No intervention yet. AI is exploring the initial map."

# Performance tracking metrics
deaths = 0
frames_survived = 0
max_survival_time = 0
global_high_score = 0

# Director evaluation timer
current_eval_interval = 20 # 2 FPS, 20 frames = 10 seconds in real world
frame_counter = 0

def get_state(x, y, hazards_lists):
     """
     The AI's Radar. Looks 1 block for every direction.
     Returns a tuple of 4 values (0 for safe, 1 for danger)
     """
     danger_up = 1 if y - GRID_SIZE < 0 or (x, y - GRID_SIZE) in hazards_lists else 0
     danger_down = 1 if y + GRID_SIZE >= WINDOW_HEIGHT or (x, y + GRID_SIZE) in hazards_lists else 0
     danger_left = 1 if x - GRID_SIZE < 0 or (x - GRID_SIZE, y) in hazards_lists else 0
     danger_right = 1 if x + GRID_SIZE >= MAZE_WIDTH or (x + GRID_SIZE, y) in hazards_lists else 0

     # States is a tuple like (1, 0, 0, 1) meaning danger UP and RIGHT
     return(danger_up, danger_down, danger_left, danger_right)


# Function to generate a new random maze
def generate_maze(px, py):
    new_hazards = {}

    # SAFE ZONE
    safe_zone = [
         (px, py),              # CENTER (Player)
         (px, py - GRID_SIZE),  # UP
         (px, py + GRID_SIZE),  # DOWN
         (px - GRID_SIZE, py),  # LEFT
         (px + GRID_SIZE, py)   # RIGHT
    ]
        
    # Loop through every possible column (X) and row (Y) in our grid
    for x in range(0, MAZE_WIDTH, GRID_SIZE):
         for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
               
               # PROTECT THE SPAWN: Don't put a hazard where the player starts!
               if (x, y) in safe_zone:
                    continue
               
               # 20% chance to spawn a hazard in the current block
               if random.random() < current_spawn_chance:
                    # Proportional lifetime. Avoids empty range error.
                    min_life = max(1, int(current_hazard_lifetime * 0.5))
                    new_hazards[(x, y)] = random.randint(min_life, current_hazard_lifetime)
    
    return new_hazards

# Create the first maze when the game starts
hazards = generate_maze(player_x, player_y)

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
        
        elif event.type == pygame.VIDEORESIZE:
             WINDOW_WIDTH = event.w
             WINDOW_HEIGHT = event.h
             MAZE_WIDTH = WINDOW_WIDTH

             screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

             if player_x >= MAZE_WIDTH: player_x = MAZE_WIDTH - GRID_SIZE
             if player_y >= WINDOW_HEIGHT: player_y = WINDOW_HEIGHT - GRID_SIZE
    
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
    if random.random() < current_spawn_chance:
        # Pick a random grid coordinate
        hx = random.randrange(0, MAZE_WIDTH, GRID_SIZE)
        hy = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)

        # Make sure it doesn't spawn ON the player or where one already exists
        if (hx, hy) != (player_x, player_y) and (hx, hy) not in hazards:
            # Use the dynamic lifetime controlled by the LLM
            hazards[(hx, hy)] = current_hazard_lifetime


    # KNOWLEDGE CYCLE
    # 1. Observe the current state (Radar)
    current_state = get_state(player_x, player_y, hazards)

    # 2. Ask the Brain what to do
    action = agent.choose_action(current_state)

    # 3. Predict where the action will take us
    next_x, next_y = player_x, player_y
    if action == 0: next_y -= GRID_SIZE     # UP
    elif action == 1: next_y += GRID_SIZE   # DOWN
    elif action == 2: next_x -= GRID_SIZE   # LEFT
    elif action == 3: next_x += GRID_SIZE   # RIGHT

    # 4. Check if the planned move is deadly (wall or hazard block)
    is_deadly = False
    if next_x < 0 or next_x >= MAZE_WIDTH or next_y < 0 or next_y >= WINDOW_HEIGHT:
         is_deadly = True # Hit a boundary wall
    elif (next_x, next_y) in hazards:
         is_deadly = True # Hit a red hazard

    # 5. Assign Rewards and Move
    if is_deadly:
         if frames_survived > global_high_score:
              global_high_score = frames_survived

         reward = -100
         deaths += 1
         frames_survived = 0
         print(f"Crash! AI Randomness (Epsilon): {agent.epsilon:.2f} | Resetting map...")
        
         # Calcula o centro do bloco que causou a morte
         crash_x = next_x + (GRID_SIZE // 2)
         crash_y = next_y + (GRID_SIZE // 2)

         # Desenha uma explosão
         pygame.draw.circle(screen, (255, 100, 0), (crash_x, crash_y), 30) # Explosão externa
         pygame.draw.circle(screen, (255, 255, 255), (crash_x, crash_y), 15) # Núcleo quente

         # Força a tela a desenha a explosão imediatamente
         pygame.display.flip()

         # Congela por 400 milissegundos
         pygame.time.delay(400)
         

         player_x = random.randrange(0, MAZE_WIDTH, GRID_SIZE)
         player_y = random.randrange(0, WINDOW_HEIGHT, GRID_SIZE)
         hazards = generate_maze(player_x, player_y) # Rebuild the world on death

    else:
         reward = 1 # Survived this step!
         frames_survived += 1

         if frames_survived > max_survival_time:
              max_survival_time = frames_survived         

         player_x, player_y = next_x, next_y # Actually move the character

    # 6. Observe the new state after moving
    next_state = get_state(player_x, player_y, hazards)

    # 7. TEACH THE BRAIN (Update the Q-Table)
    agent.learn(current_state, action, reward, next_state)

    # 8. The Director Intervenes
    frame_counter += 1
    if frame_counter >= current_eval_interval:
         print("\n --- LLM EVALUATION TRIGGERED ---")

         # RPG style dice roll (D20)
         agent_roll = random.randint(1, 20)
         director_roll = random.randint(1, 20)
         print(f"[CLASH] Agent rolled: {agent_roll} | Director rolled: {director_roll}")

         if agent_roll > director_roll:
              print("[CLASH] Agent Wins! Intervention blocked. Gaining time to learn...")
              deaths = 0
              max_survival_time = 0
              frame_counter = 0
              print("--------------------------------\n")

         else:              
            print("[CLASH] Director Wins! Invoking Groq to alter the matrix...")
            # Call the LLM API via our Director class
            new_rules = director.evaluate_performance(deaths, max_survival_time, agent.epsilon)

            # Apply the new rules returned by the LLM
            new_spawn = new_rules.get("spawn_chance", current_spawn_chance)
            new_lifetime = new_rules.get("hazard_lifetime", current_hazard_lifetime)
            current_llm_reasoning = new_rules.get("reasoning", "Default difficulty adjustment.")

            # --- DYNAMIC EPSILON SHOCK ---
            spawn_increase = new_spawn - current_spawn_chance

            if (spawn_increase > 0 or new_lifetime < current_hazard_lifetime) and agent.epsilon < 0.50:
                # Math of shock: 0.10 base + 1.5 * hazard increase
                extra_shock = max(0, spawn_increase) * 1.5
                dynamic_shock = 0.05 + extra_shock

                dynamic_shock = min(dynamic_shock, 0.30)

                agent.epsilon = min(agent.epsilon + dynamic_shock, 0.85)
                print(f"[ADAPTATION] Hostile environment! Dynamic shock of +{dynamic_shock:.2f}. New Epsilon: {agent.epsilon:.2f}")
                
            # Apply the new rules 
            current_spawn_chance = new_spawn
            current_hazard_lifetime = new_lifetime

            # --- Dynamic Pacing --- 
            base_interval = 20 # 10 seconds base (at 2 FPS)

            if agent.epsilon > 0.5:
                current_eval_interval = int(base_interval * 1.5)
                print("[PACE] AI is exploring. The Director will wait longer before changing the map.")
            elif agent.epsilon < 0.2:
                current_eval_interval = int(base_interval * 0.7)
                print("[PACE] AI is too confident. The next map change will come sooner.")
            else:
                current_eval_interval = base_interval
        
            # Reset the metrics for the new evaluation epoch
            deaths = 0
            max_survival_time = 0
            frame_counter = 0
            print("--------------------------------\n")


    # --------------------------------------
    # C. RENDERING (DRAWING TO SCREEN)
    # --------------------------------------
    # 1. Clear the screen from the previous frame
    screen.fill((15, 15, 20))

    # linhas verticais
    for x in range(0, MAZE_WIDTH, GRID_SIZE):
         pygame.draw.line(screen, (30, 30, 40), (x, 0), (x, WINDOW_HEIGHT), 1)

    # Linhas horizontais
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
         pygame.draw.line(screen, (30, 30, 40), (0, y), (MAZE_WIDTH, y), 1)       

    time_now = pygame.time.get_ticks()
    pulse = (math.sin(time_now / 200.0) + 1) / 2.0

    # Draw all hazards using a loop
    for h_x, h_y in hazards:
         center_x = h_x + (GRID_SIZE // 2)
         center_y = h_y + (GRID_SIZE // 2)

         time_offset = h_x + h_y
         mine_pulse = (math.sin((time_now + time_offset * 5) / 150.0) + 1) / 2.0
         
         glow_radius = int(10 + (mine_pulse * 6)) 
         
         # Base escura da mina
         pygame.draw.circle(screen, (80, 20, 20), (center_x, center_y), 16)
         
         # Brilho de energia (Pulsação)
         pygame.draw.circle(screen, (255, 50, 50), (center_x, center_y), glow_radius)
         
         # Núcleo de calor (Amarelo/Branco)
         pygame.draw.circle(screen, (255, 200, 100), (center_x, center_y), 6) 
         
         # Detalhe técnico: um "X" marcando a mina
         pygame.draw.line(screen, (255, 100, 100), (h_x + 8, h_y + 8), (h_x + GRID_SIZE - 8, h_y + GRID_SIZE - 8), 2)
         pygame.draw.line(screen, (255, 100, 100), (h_x + GRID_SIZE - 8, h_y + 8), (h_x + 8, h_y + GRID_SIZE - 8), 2) 
         
    # Robot
    # Esteiras/Rodas laterais
    pygame.draw.rect(screen, (100, 100, 100), (player_x + 4, player_y + 14, 6, 20), border_radius=3)
    pygame.draw.rect(screen, (100, 100, 100), (player_x + 30, player_y + 14, 6, 20), border_radius=3)

    # Corpo principal metálico
    body_rect = (player_x + 8, player_y + 10, 24, 24)
    pygame.draw.rect(screen, (50, 120, 220), body_rect, border_radius=5)

    # Visor (Tela preta)
    pygame.draw.rect(screen, (20, 20, 30), (player_x + 12, player_y + 16, 16, 8))

    # Cor do olho (XAI visual: Muda de acordo com a Epsilon / Confiança do Agente)
    if agent.epsilon > 0.6:
         eye_color = (255, 200, 0) # Amarelo / IA explorando/confusa
    elif agent.epsilon < 0.3:
         eye_color = (50, 255, 50) # Verde / IA confiante/Aprendeu o mapa
    else:
         eye_color = (0, 255, 255) # Ciano/ Estado normal de aprendizado

    # Desenha o olho piscando no visor
    eye_width = 12 if pulse > 0.1 else 2 # Animação de "piscar"
    pygame.draw.rect(screen, eye_color, (player_x + 20 - (eye_width // 2), player_y + 18, eye_width, 4))

    # Antena de comunicação com a Groq
    pygame.draw.line(screen, LIGHT_GRAY, (player_x + 20, player_y + 10), (player_x + 20, player_y + 2), 2)
    # Bolinha da antena
    antenna_color = RED if pulse > 0.5 else (100, 0, 0)
    pygame.draw.circle(screen, antenna_color, (player_x + 20, player_y + 2), 3)

    # --- DRAWING THE HUD (Heads-Up Display) ---
    # A. Current window size
    current_w, current_h = screen.get_size()
    hud_height = 95 # Bottom panel height

    # B. Semi-transparent layer
    hud_surface = pygame.Surface((current_w, hud_height))
    hud_surface.set_alpha(220) # 0 is invisible, 255 is solid, 220 gives a dark background
    hud_surface.fill(BLACK)

    # C. Draw the transparent layer at the bottom of the screen
    screen.blit(hud_surface, (0, current_h - hud_height))

    # D. Subtle dividing line at the top of the HUD
    pygame.draw.line(screen, LIGHT_GRAY, (0, current_h - hud_height), (current_w, current_h - hud_height), 1)

    # E. Organizing text horizontally (3 columns)
    pad_y = current_h - hud_height + 15 # Top margin

    # F. Agent Status Column
    col1_x = 20
    screen.blit(font_main.render("Q-Learning AI", True, WHITE), (col1_x, pad_y))
    screen.blit(font_main.render(f"Time: {format_time(frames_survived)}", True, LIGHT_GRAY), (col1_x, pad_y + 26))
    screen.blit(font_main.render(f"High Score: {format_time(global_high_score)}", True, (255, 215, 0)), (col1_x, pad_y + 48))
    pygame.draw.line(screen, (70, 70, 70), (240, pad_y), (240, current_h - 15), 1)
    
    # G. LLM Director Column
    col2_x = 260
    screen.blit(font_main.render("LLM Decision Rules (Groq)", True, WHITE), (col2_x, pad_y))
    screen.blit(font_main.render(f"Exploration (Epsilon): {agent.epsilon:.2f}", True, LIGHT_GRAY), (col2_x, pad_y + 26))
    screen.blit(font_small.render(f"Spawn Rate: {int(current_spawn_chance * 100)}%", True, (255, 100, 100)), (col2_x, pad_y + 48))
    pygame.draw.line(screen, (70, 70, 70), (580, pad_y), (580, current_h - 15), 1)

    # H. XAI Logs Column
    col3_x = 600
    log_title = font_main.render("Groq Decision Log", True, WHITE)
    screen.blit(log_title, (col3_x, pad_y))

    tag_x = col3_x + log_title.get_width() + 10
    
    xai_tag = font_small.render("• Natural Language Translation", True, (100, 200, 255)) # Ciano
    screen.blit(xai_tag, (tag_x, pad_y + 2))

    # H1. Wraps LLM text into lines of max 85 characters
    wrapped_reasoning = textwrap.wrap(current_llm_reasoning, width=70)

    # H2. Draws each line one below the other
    for i, line in enumerate(wrapped_reasoning):
        texto_renderizado = font_small.render(line, True, (180, 255, 180))
        screen.blit(texto_renderizado, (col3_x, pad_y + 26 + (i * 20)))

    # ------------------------------------------------------

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