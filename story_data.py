# --- COLOR SETTINGS ---
# These are ANSI escape codes that change the text color in the terminal.
# We define them here so the 'world_map' can use them easily.
BLUE = r"\033[94m"
GREEN = r"\033[92m"
RED = r"\033[91m"
GOLD = r"\033[93m"
BOLD = r"\033[1m"
END = r"\033[0m" # This 'resets' the color back to normal white

world_map = {
    "docks": {
        "text": "The Iron Port is cold today.\nTo the 'north' is the Market. You see a 'sword' on the ground.\nYou also see an angry sailer looking for a 'fight' weilding a shiny cog. You might need that!",
        "post_item_text": "The Iron Port is cold today.\nTo the 'north' is the Market.\nThat angry sailor looks ready to 'fight' for that sword of yours.",
        "alt_text": "The Iron Port is cold today. The docks are quiet now that the sailor is gone.\nHeading 'north' to the market might be a better idea.",
        "choices": {"north": "market", 
                    "sword": "get_item",
                    "fight": "docks",
                    },
        "item": "sword",
        "enemy": "Angry Sailor",
        "enemy_hp": 30,
        "loot": "Brass_Cog"
    },
    "market": {
        "text": "The Market is loud. To the 'east' is a massive Clock Tower. To the 'south' are the docks.",
        "choices": {"east": "clock_tower", "south": "docks"}
    },
    "clock_tower": {
        "text": "The Tower door is locked. A slot on the door looks like it fits a cog.",
        "choices": {"unlock": "top_floor", "back": "market"},
        "required_item": "Brass Cog"
    },
    "top_floor": {
        "text": "You reached the top! The view of the city is incredible. YOU WIN!",
        "choices": {}
    },
    "tavern": {
        "text": f"{BOLD}THE RUSTY TANKARD{END}\n"
                "Warmth hits you instantly, smelling of roasted meat and spilled ale. The floor is "
                "sticky under your boots, and the low hum of conversation dies down as you enter. "
                "The barkeep eyes your satchel. 'Looking for the 'sewer_key'?' he mutters.",
        "choices": {"back": "market"}
    },
    "dark_alley": {
    "text": f"{RED}You wander into a dead end. A group of bandits surrounds you. This was a mistake.{END}",
    "choices": {}, # No choices means the game loop ends
    "status": "dead" 
    },
}