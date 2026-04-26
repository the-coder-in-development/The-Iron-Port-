import sys, time
import json
import random
import os

def speak(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02) # Fast enough to read, slow enough to feel "cool"
    print()

# utils.py additions

HEADER = r"\033[95m]"
BLUE = r"\033[94m]"
GREEN = r"\033[92m]"
RED = r"\033[91m]"
BOLD = r"\033[1m]"
END = r"\033[0m]" # Always use this to 'reset' the color back to white

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def save_game(location, inventory, health):
    data = {
        "location": location,
        "inventory": inventory,
        "health": health
    }
    with open("savegame.json", "w") as f:
        json.dump(data, f)
    print("--- Game Progress Saved! ---")

def load_game():
    try:
        with open("savegame.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    
def show_achievement(name, description):
    print("\n" + "*" * 40)
    print(f"🏆 ACHIEVEMENT UNLOCKED: {name}")
    print(f"📜 {description}")
    print("*" * 40 + "\n")
    time.sleep(1) # Give you a second to soak in the glory!

def draw_health_bar(current_hp, max_hp):
    bar_length = 20
    # Calculate how many "blocks" to fill
    filled_length = int(bar_length * current_hp // max_hp)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    
    color = "\033[92m" # Green
    if current_hp < 30: color = "\033[91m" # Red if low
    
    print(f"HP: {color}[{bar}] {current_hp}/{max_hp}\033[0m")

def enter_combat(player_health, enemy_name, enemy_hp, inventory):
    has_shield = "Shield" in inventory 
    speak(f" A WILD {enemy_name} APPEARS! ")
    
    while enemy_hp > 0 and player_health > 0:
        print(f" {enemy_name}: {enemy_hp} HP | You: {player_health} HP")
        action = input("Will you [attack], [block], or [flee]?"). lower().strip()

        if action == "flee":
            speak("You turn and run back to safety!")
            return player_health, True

        player_damage = random.randint(10, 20)
        enemy_damage = random.randint(5, 15)

        if action == "attack":
            enemy_hp -= player_damage
            speak(f"You swing your sword for {player_damage} damage!")
            if enemy_hp > 0:    
                player_health -= enemy_damage
                speak(f"The {enemy_name} strike back for {enemy_damage} damage!")
        
        elif action == "block":
            if has_shield:
                reduced_damage = enemy_damage // 2
                player_health -= reduced_damage
                speak(f"You raise your shield! You only take {reduced_damage} damage.")
            else:
                player_health -= enemy_damage
                speak(f"You tried to block without a shield! You took full damage ({enemy_damage}).")

    if player_health > 0:
        speak(f"Victory! The {enemy_name} has been defeated.")
        return player_health, False 
    else:
        return 0, False