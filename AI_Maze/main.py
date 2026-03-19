import pygame
import sys
import random
import textwrap
import math
import threading
from agent import QLearningAgent
from director import GameDirector

# ====================================
# 1. CONFIGURATION & CONSTANTS
# ====================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAZE_WIDTH = WINDOW_WIDTH
GRID_SIZE = 40          # The world is divided into 40x40 pixel blocks
FPS = 60                # Game speed slowed down to watch the AI learn
TICK_RATE = 2           # A IA toma 2 decisões por segundo
TICK_DELAY = 1000 // TICK_RATE      # Tempo em milissegundos entre as decisões

# RGB Color Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 100, 255)    # Agent
RED = (200, 50, 50)     # Hazard
DARK_GREY = (30, 30, 30)

# Convert frames into clock's time (MM:SS)
def format_time(frames):
     total_seconds = frames // TICK_RATE
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

# Variáveis para desenho suave
draw_x = float(player_x)
draw_y = float(player_y)
prev_x = float(player_x)
prev_y = float(player_y)


# Relógio interno para controlar o cérebro da IA
last_tick_time = pygame.time.get_ticks()

# Actions: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT, 4=UP-LEFT, 5=UP-RIGHT, 6=DOWN-LEFT, 7=DOWN-RIGHT
agent = QLearningAgent(actions=[0, 1, 2, 3, 4, 5, 6, 7])

# AI Game Director & Metrics
director = GameDirector()

# Mutable environment variables (controlled by the LLM)
current_spawn_chance = 0.02
current_hazard_lifetime = 20
current_llm_reasoning = "System Onboarding: Low hazards to allow safe initial exploration."
is_awaiting_director = False
current_agent_log = "Action: [START] • System initialized. Waiting for data."

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
     look_up_y = (y - GRID_SIZE) % WINDOW_HEIGHT
     look_down_y = (y + GRID_SIZE) % WINDOW_HEIGHT
     look_left_x = (x - GRID_SIZE) % MAZE_WIDTH
     look_right_x = (x + GRID_SIZE) % MAZE_WIDTH

     danger_up = 1 if (x, look_up_y) in hazards_lists else 0
     danger_down = 1 if (x, look_down_y) in hazards_lists else 0
     danger_left = 1 if (look_left_x, y) in hazards_lists else 0
     danger_right = 1 if (look_right_x, y) in hazards_lists else 0

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

def director_worker(deaths_snapshot, time_snapshot, epsilon_snapshot):
     global current_spawn_chance, current_hazard_lifetime, current_llm_reasoning
     global current_eval_interval, is_awaiting_director

     try:
          new_rules = director.evaluate_performance(deaths_snapshot, time_snapshot, epsilon_snapshot)

          new_spawn = new_rules.get("spawn_chance", current_spawn_chance)
          new_lifetime = new_rules.get("hazard_lifetime", current_hazard_lifetime)

          current_llm_reasoning = new_rules.get("reasoning", "Default difficulty adjustment.")

          spawn_increase = new_spawn -current_spawn_chance
          if (spawn_increase > 0 or new_lifetime < current_hazard_lifetime) and agent.epsilon < 0.50:
               extra_shock = max(0, spawn_increase) * 1.5
               dynamic_shock = min(0.05 + extra_shock, 0.30)
               agent.epsilon = min(agent.epsilon + dynamic_shock, 0.85)
               print(f"[ADAPTATION] Hostile environment! Epsilon increased to: {agent.epsilon:.2f}")
         
          # Atualiza o mundo
          current_spawn_chance = new_spawn
          current_hazard_lifetime = new_lifetime

          # Atualiza o ritmo
          base_interval = 20
          if agent.epsilon > 0.5: current_eval_interval = int(base_interval * 1.5)
          elif agent.epsilon < 0.2: current_eval_interval = int(base_interval * 0.7)
          else: current_eval_interval = base_interval

     except Exception as e:
          print(f"[THREAD ERROR] Failed to contact Groq: {e}")
    
     is_awaiting_director = False

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
    current_time = pygame.time.get_ticks()

    if current_time - last_tick_time >= TICK_DELAY:
         prev_x = float(player_x)
         prev_y = float(player_y)

         last_tick_time = current_time
    
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

         # Pega os valores matemáticos daquele exato momento (8 ações possíveis)
         q_vals = agent.q_table.get(current_state, [0.0] * 8)
         chosen_q = q_vals[action]

         # Traduz a Ação
         dirs = ["UP", "DOWN", "LEFT", "RIGHT", "UP-LEFT", "UP-RIGHT", "DOWN-LEFT", "DOWN-RIGHT"]
         action_str = dirs[action]

         # Natural Language Log
         if chosen_q == 0.0:
             nl_text = f"No data. Exploring {action_str} randomly."
         elif chosen_q > 0:
             nl_text = f"Safe path known. Moving {action_str}."
         else:
             nl_text = f"Danger detected! Evading {action_str}."
        
         current_agent_log = f"Action: [{action_str}] • {nl_text}"

        # 3. Predict where the action will take us
         next_x, next_y = player_x, player_y
         if action == 0: next_y -= GRID_SIZE     # UP
         elif action == 1: next_y += GRID_SIZE   # DOWN
         elif action == 2: next_x -= GRID_SIZE   # LEFT
         elif action == 3: next_x += GRID_SIZE   # RIGHT
         elif action == 4: # UP-LEFT
              next_x -= GRID_SIZE
              next_y -= GRID_SIZE
         elif action == 5: # UP-RIGHT
              next_x += GRID_SIZE
              next_y -= GRID_SIZE
         elif action == 6: # DOWN-LEFT
              next_x -= GRID_SIZE
              next_y += GRID_SIZE
         elif action == 7: # DOWN-RIGHT
              next_x += GRID_SIZE
              next_y += GRID_SIZE

        # Pac Man Effect
         next_x = next_x % MAZE_WIDTH
         next_y = next_y % WINDOW_HEIGHT

        # 4. Check if the planned move is deadly (wall or hazard block)
         is_deadly = False
         if (next_x, next_y) in hazards:
             is_deadly = True # Hit a red hazard

        # 5. Assign Rewards and Move
         if is_deadly:
            if frames_survived > global_high_score:
                global_high_score = frames_survived

            reward = -100
            deaths += 1
            frames_survived = 0
            print(f"Crash! AI Randomness (Epsilon): {agent.epsilon:.2f} | Resetting map...")

            draw_x = float(next_x)
            draw_y = float(next_y)

            body_rect = (draw_x + 8, draw_y + 10, 24, 24)
            pygame.draw.rect(screen, (50, 120, 220), body_rect, border_radius=5)
            
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
            draw_x = float(player_x)
            draw_y = float(player_y)
            prev_x = float(player_x)
            prev_y = float(player_y)
            hazards = generate_maze(player_x, player_y) # Rebuild the world on death

         else:
            reward = 1 # Survived this step!
            frames_survived += 1

            if frames_survived > max_survival_time:
                max_survival_time = frames_survived         

            player_x, player_y = next_x, next_y # Actually move the character

        # Wrap-around Lerp
         if player_x - prev_x > GRID_SIZE * 2: # Foi para a esquerda dando a volta
             prev_x += MAZE_WIDTH
         elif prev_x - player_x > GRID_SIZE * 2: # Foi para a direita dando a volta
             prev_x -= MAZE_WIDTH

         if player_y - prev_y > GRID_SIZE * 2: # Foi para cima dando a volta
             prev_y += WINDOW_HEIGHT
         elif prev_y - player_y > GRID_SIZE * 2: # Foi para baixo dando a volta
             prev_y -= WINDOW_HEIGHT         

        # 6. Observe the new state after moving
         next_state = get_state(player_x, player_y, hazards)

        # 7. TEACH THE BRAIN (Update the Q-Table)
         agent.learn(current_state, action, reward, next_state)

        # 8. The Director Intervenes
         frame_counter += 1
         if frame_counter >= current_eval_interval and not is_awaiting_director:
            print("\n --- LLM EVALUATION TRIGGERED ---")

            # RPG style dice roll (D20)
            agent_roll = random.randint(1, 20)
            director_roll = random.randint(1, 20)
            print(f"[CLASH] Agent rolled: {agent_roll} | Director rolled: {director_roll}")

            if agent_roll > director_roll:
                print("[CLASH] Agent Wins! Intervention blocked. Gaining time to learn...")              
                print("--------------------------------\n")

            else:              
                print("[CLASH] Director Wins! Invoking Groq to alter the matrix...")
                # Call the LLM API via our Director class
                
                is_awaiting_director = True

                thread = threading.Thread(target=director_worker, args=(deaths, max_survival_time,agent.epsilon))
                thread.daemon = True
                thread.start()
            
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
         
    progress = (time_now - last_tick_time) / TICK_DELAY
    progress = min(progress, 1.0)

    draw_x = prev_x + (player_x - prev_x) * progress
    draw_y = prev_y + (player_y - prev_y) * progress

    # Robot
    # Esteiras/Rodas laterais
    pygame.draw.rect(screen, (100, 100, 100), (draw_x + 4, draw_y + 14, 6, 20), border_radius=3)
    pygame.draw.rect(screen, (100, 100, 100), (draw_x + 30, draw_y + 14, 6, 20), border_radius=3)

    # Corpo principal metálico
    body_rect = (draw_x + 8, draw_y + 10, 24, 24)
    pygame.draw.rect(screen, (50, 120, 220), body_rect, border_radius=5)

    # Visor (Tela preta)
    pygame.draw.rect(screen, (20, 20, 30), (draw_x + 12, draw_y + 16, 16, 8))

    # Cor do olho (XAI visual: Muda de acordo com a Epsilon / Confiança do Agente)
    if agent.epsilon > 0.6:
         eye_color = (255, 200, 0) # Amarelo / IA explorando/confusa
    elif agent.epsilon < 0.3:
         eye_color = (50, 255, 50) # Verde / IA confiante/Aprendeu o mapa
    else:
         eye_color = (0, 255, 255) # Ciano/ Estado normal de aprendizado

    # Desenha o olho piscando no visor
    eye_width = 12 if pulse > 0.1 else 2 # Animação de "piscar"
    pygame.draw.rect(screen, eye_color, (draw_x + 20 - (eye_width // 2), draw_y + 18, eye_width, 4))

    # Antena de comunicação com a Groq
    pygame.draw.line(screen, LIGHT_GRAY, (draw_x + 20, draw_y + 10), (draw_x + 20, draw_y + 2), 2)
    # Bolinha da antena
    antenna_color = RED if pulse > 0.5 else (100, 0, 0)
    pygame.draw.circle(screen, antenna_color, (draw_x + 20, draw_y + 2), 3)

    # --- DRAWING THE HUD (Heads-Up Display) ---
    # A. Current window size
    current_w, current_h = screen.get_size()
    hud_height = 150 # Bottom panel height

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
    col1_center = 120
    
    t1 = font_main.render("Q-Learning AI", True, WHITE)
    screen.blit(t1, t1.get_rect(center=(col1_center, pad_y + 10)))

    t2 = font_main.render(f"Time: {format_time(frames_survived)}", True, LIGHT_GRAY)
    screen.blit(t2, t2.get_rect(center=(col1_center, pad_y + 36)))

    t3 = font_main.render(f"High Score: {format_time(global_high_score)}", True, (255, 215, 0))
    screen.blit(t3, t3.get_rect(center=(col1_center, pad_y + 58)))

    pygame.draw.line(screen, (70, 70, 70), (240, pad_y), (240, current_h - 15), 1)
    
    # G. LLM Director Column
    col2_center = 410
    
    t4 = font_main.render("LLM Decision Rules (Groq)", True, WHITE)
    screen.blit(t4, t4.get_rect(center=(col2_center, pad_y + 10)))
    
    t5 = font_main.render(f"Exploration (Epsilon): {agent.epsilon:.2f}", True, LIGHT_GRAY)
    screen.blit(t5, t5.get_rect(center=(col2_center, pad_y + 36)))
    
    t6 = font_small.render(f"Spawn Rate: {int(current_spawn_chance * 100)}%", True, (255, 100, 100))
    screen.blit(t6, t6.get_rect(center=(col2_center, pad_y + 58)))
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

    agent_y = pad_y + 75

    agent_title = font_main.render("Agent Thought Process (Q-Table)", True, WHITE)
    screen.blit(agent_title, (col3_x, agent_y))

    text_agent = font_small.render(current_agent_log, True, (180, 255, 180))
    screen.blit(text_agent, (col3_x, agent_y + 24))

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