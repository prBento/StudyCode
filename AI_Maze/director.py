import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 1. Open our invisible vault and load the environment variables
load_dotenv()

class GameDirector:
    def __init__(self):
        # Initialize the OpenAI client.
        #self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # We use gpt-4o-mini as it is incredibly fast, smart, and cost-effective for JSON tasks
        #self.model_id = 'gpt-4o-mini'

    # We use the OpenAI library, but point it to Groq's free, blazing-fast servers!
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        
        self.model_id = 'llama-3.1-8b-instant'  

    def evaluate_performance(self, deaths, max_survival_time, current_epsilon):
        """
        Sends the Agent's statistics to the LLM and asks for new game rules.
        Returns a dictionary with the new 'spawn_chance' and 'hazard_lifetime'.
        """
        print("\n[DIRECTOR] Analyzing AI performance with Groq...")
        
        # --- PROMPT ENGINEERING ---
        prompt = f"""
        You are the Game Director of a dynamic maze.
        The player is a Q-Learning Artificial Intelligence learning to survive.
        
        Here are the player's current stats:
        - Deaths: {deaths}
        - Max survival time (in frames): {max_survival_time}
        - Epsilon Rate (Randomness. 1.0 is exploring/dumb, near 0.0 is smart): {current_epsilon:.2f}

        Based on this data, adjust the game difficulty to keep the AI engaged:
        - If it dies too much or Epsilon is high, make it easier (lower spawn_chance, higher hazard_lifetime).
        - If it survives for a long time and Epsilon is low, make the game much harder!
        
        Strict limits you must follow:
        - spawn_chance: float number between 0.05 and 0.50
        - hazard_lifetime: integer between 10 and 100

        Respond EXCLUSIVELY with a valid JSON object.
        Use exactly this structure:
        {{
            "spawn_chance": <float_value>,
            "hazard_lifetime": <int_value>,
            "reasoning": "<Write a short sentence in English explaining why you chose these numbers. Max 60 characters!>"
        }}
        """

        try:
            # Send the prompt using the OpenAI SDK
            response = self.client.chat.completions.create(
                model=self.model_id,
                response_format={ "type": "json_object" }, # Forces the model to output valid JSON
                messages=[
                    {"role": "system", "content": "You are a game server that outputs strictly JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract the string content from OpenAI's response
            response_text = response.choices[0].message.content
            
            # Convert the JSON string into a real Python Dictionary
            new_rules = json.loads(response_text)
            print(f"[DIRECTOR] New rules defined: {new_rules}")
            return new_rules
            
        except Exception as e:
            # Fail-safe system: If the internet drops or API fails, the game doesn't crash
            print(f"[DIRECTOR ERROR] Failed to contact the API: {e}")
            print("[DIRECTOR] Keeping default difficulty for safety.")
            return {"spawn_chance": 0.10, "hazard_lifetime": 50}





#import json
#from google import genai
#from dotenv import load_dotenv
#
## 1. Open our invisible vault and load the environment variables
#load_dotenv()
#
#class GameDirector:
#    def __init__(self):
#        # The new Google GenAI SDK automatically picks up the GEMINI_API_KEY from the .env file.
#        # We instantiate a Client instead of configuring a global module.
#        self.client = genai.Client()
#        
#        # We use a modern model version. 
#        self.model_id = 'gemini-2.0-flash'
#
#    def evaluate_performance(self, deaths, max_survival_time, current_epsilon):
#        """
#        Sends the Agent's statistics to the LLM and asks for new game rules.
#        Returns a dictionary with the new 'spawn_chance' and 'hazard_lifetime'.
#        """
#        print("\n[DIRECTOR] Analyzing AI performance...")
#        
#        # --- PROMPT ENGINEERING ---
#        prompt = f"""
#        You are the Game Director of a dynamic maze.
#        The player is a Q-Learning Artificial Intelligence learning to survive.
#        
#        Here are the player's current stats:
#        - Deaths: {deaths}
#        - Max survival time (in frames): {max_survival_time}
#        - Epsilon Rate (Randomness. 1.0 is exploring/dumb, near 0.0 is smart): {current_epsilon:.2f}
#
#        Based on this data, adjust the game difficulty to keep the AI engaged:
#        - If it dies too much or Epsilon is high, make it easier (lower spawn_chance, higher hazard_lifetime).
#        - If it survives for a long time and Epsilon is low, make the game much harder!
#        
#        Strict limits you must follow:
#        - spawn_chance: float number between 0.05 and 0.50
#        - hazard_lifetime: integer between 10 and 100
#
#        Respond EXCLUSIVELY with a valid JSON object. Do not include markdown code blocks around it.
#        Use exactly this structure:
#        {{
#            "spawn_chance": <float_value>,
#            "hazard_lifetime": <int_value>
#        }}
#        """
#
#        try:
#            # Send the prompt using the new SDK syntax
#            response = self.client.models.generate_content(
#                model=self.model_id,
#                contents=prompt
#            )
#            
#            # Security cleanup: Remove markdown backticks (```json ... ```) if the LLM adds them
#            cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
#            
#            # Convert the JSON string into a real Python Dictionary
#            new_rules = json.loads(cleaned_text)
#            print(f"[DIRECTOR] New rules defined: {new_rules}")
#            return new_rules
#            
#        except Exception as e:
#            # Fail-safe system: If the internet drops or API fails, the game doesn't crash
#            print(f"[DIRECTOR ERROR] Failed to contact the API: {e}")
#            print("[DIRECTOR] Keeping default difficulty for safety.")
#            return {"spawn_chance": 0.10, "hazard_lifetime": 50}

        