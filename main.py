from story_data import world_map
from utils import speak, clear_screen, save_game, load_game, show_achievement, enter_combat
import random

inventory = []
current_location = "docks"
achievements = []
health = 100

def main_menu():
    global current_location, inventory, health
    
    while True:
        clear_screen()
        print("================================")
        print("    THE IRON PORT CHRONICLES    ")
        print("================================")
        print("  1. [PLAY] New Adventure")
        print("  2. [LOAD] Resume Journey")
        print("  3. [QUIT] Exit Game")
        print("================================")
        
        choice = input("\n> ").lower().strip()
        
        if choice in ["1", "play"]:
            clear_screen()
            speak("--- WELCOME TO THE IRON PORT ---")
            speak("Type 'help' at any time if you are stuck!")
            speak("Type the words in 'quotes' to move or interact.")
            speak("Type 'inventory' to see what you are carrying.")
            speak("Type 'look' to see the room description again.")
            speak("The fog lifts as you arrive at the docks...")
            input("[ Press Enter to begin your story... ]")
            return # Exit menu and start the game
            
        elif choice in ["2", "load"]:
            data = load_game()
            if data:
                current_location = data["location"]
                inventory = data["inventory"]
                # If you added health to your save_game function:
                health = data.get("health", 100)
                speak("Records retrieved. Your journey continues...")
                break
            else:
                speak("No previous records found in the archives.")
                
        elif choice in ["3", "quit"]:
            speak("Farewell, traveler.")
            exit()

# Check if a save file exists on the computer
save_data = load_game()

if save_data:
    print("--- OLD RECORDS FOUND ---")
    load_choice = input("Would you like to resume your journey? (y/n): ").lower().strip()
    if load_choice == 'y':
        current_location = save_data["location"]
        inventory = save_data["inventory"]
        achievements = save_data.get("achievements", [])
        clear_screen()
        speak(f"Welcome back. You are currently in the {current_location}.")
    else:
        speak("Starting a new adventure...")
        # If they say no, the variables stay at "docks" and empty []

main_menu()

while True:
    if health <= 0:
        speak(f"Your strength fades... the journey ends here.")
        speak("--- GAME OVER ---")
        break # This exits the loop gracefully

    location_data = world_map[current_location]
    # Check what state the room is in (Item gone > Enemy gone > Default)
    # 1. PRIORITY: If the item is picked up, show the final version
    if "post_item_text" in location_data and "item" not in location_data:
        speak("\n" + location_data["post_item_text"])
    # 2. SECONDARY: If only the enemy is gone, show the alt_text
    elif "alt_text" in location_data and "enemy" not in location_data:
        speak("\n" + location_data["alt_text"])
    # 3. DEFAULT: Show the original text
    else:
        speak("\n" + location_data["text"])

    # Check if the room has no more choices (Game Over / Victory)
    if not location_data["choices"]:
        speak("\n--- THE END ---")
        break

    choice = input("\n[Action]: ").lower().strip()

    # --- THE SYSTEM COMMANDS ---
    if choice == "help":
        speak("\n--- HELP MENU ---")
        speak("* Type the words in 'quotes' to move or interact.")
        speak("* Type 'inventory' to see what you are carrying.")
        speak("* Type 'look' to see the room description again.")
        speak(f"* Available paths here: {list(location_data['choices'].keys())}")

    elif choice == "inventory":
        if not inventory:
            speak("Your pockets are empty.")
        else:
            speak(f"You are carrying: {', '.join(inventory)}")

    elif choice == "look":
        continue # Just loops back to print the room text again

    elif choice == "save":
        save_game(current_location, inventory, health)

    if choice == "python_master":
        show_achievement("The Chosen One", "You remembered the secret word from Coder Club!")
        speak(f"A secret passage opens! You found the Developer's Cache.")
        inventory.append("Master Key")
        speak("*** Master Key added to inventory. You can now open any door! ***")
        continue

    elif choice == "map": # A secret tool for the student 'Developers'
        speak(f"Dev Mode: The rooms in this world are: {list(world_map.keys())}")

    # --- THE GAME LOGIC ---
    elif choice == "get_item" and "item" in location_data:
        item_name = location_data["item"]
        inventory.append(item_name)
        speak(f"*** You picked up the {item_name}! ***")
        del location_data["item"]
        choices_to_remove = [k for k, v in location_data["choices"].items() if v == "get_item"]
        for key in choices_to_remove:
            del location_data["choices"][key]
        continue 

    elif choice in location_data["choices"]:
        dest_name = location_data["choices"][choice]

        # 1. Handle Combat (If the player chose to fight)
        if choice == "fight" and "enemy" in location_data:
            result = enter_combat(health, location_data["enemy"], location_data["enemy_hp"], inventory)
            health, fled = result if isinstance(result, tuple) else (result, False)
            if fled or health <= 0:
                continue

            if health > 0 and not fled:
                speak("You defeated the sailor!")
                if "loot" in location_data:
                    item_found = location_data["loot"]
                    inventory.append(item_found)
                    speak(f"You picked up: {item_found}!")
                    del location_data["loot"]
            
            if "enemy" in location_data:
                del location_data["enemy"]
            current_location = dest_name
            continue

        # 2. Handle Item Pickups (If the choice was the item name)
        if dest_name == "get_item":
            if "item" in location_data:
                item_name = location_data["item"]
                inventory.append(item_name)
                speak(f"*** You picked up the {item_name}! ***")
                del location_data["item"]
                choices_to_remove = [k for k, v in location_data["choices"].items() if v == "get_item"]
                for key in choices_to_remove:
                    del location_data["choices"][key]
            else:
                speak("There is nothing left to pick up here.")
            continue # <--- This prevents the "Traveling" crash

        # 3. Handle Normal Movement & Locked Doors
        dest_data = world_map[dest_name]
        if "required_item" in dest_data:
            if dest_data["required_item"] in inventory:
                speak(f"--- You use the {dest_data['required_item']}! ---")
                current_location = dest_name
                clear_screen()
            else:
                speak(f"--- Access Denied: You need the {dest_data['required_item']}. ---")
        else:
            if current_location != dest_name:
                clear_screen()
                speak("---Traveling...---")
                current_location = dest_name

    else:
        speak("I don't understand that. Type 'help' for tips.")