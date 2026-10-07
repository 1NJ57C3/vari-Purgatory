import random
import time
import psutil

from data.rooms import rooms
from data.items import church_have_items, redchapel_have_items, whitechapel_have_items, blackchapel_have_items
from data.knowings import shortest_knowing, technical_shortest, longest_knowing

from utils.help import print_instructions
from utils.load import load_game
from utils.save import save_game


class GameState:
    def __init__(self):
        self.inventory = []

        @property
        def room(self):
            return self._room

        @room.setter
        def room(self, number: int):
            self._room = rooms[number]


def get_next_action(sequence):
    if sequence:
        return sequence.pop(0)
    else:
        return "quit"


current_room = 0
inventory = []

def print_room_actions():
    actions = rooms[current_room]["actions"]
    for action in actions:
        print ("-", action)


def print_room_descriptions():
    descriptions = rooms[current_room]["description"]
    print_list(descriptions)

def print_list(list):
    for item in list:
        print(item)
        input()


# Instructions
print_instructions()
game_state = input("> ")

# Start CPU monitoring
initial_cpu = psutil.cpu_times()
# Gets the CPU times specifically for the current process
initial_process_cpu = psutil.Process().cpu_times()
# records the time when the game starts
start_time = time.time()

if game_state.lower() == "load":
    load_game()
    print_room_descriptions()
    print_room_actions()
else:
    # Starting room
    print_room_descriptions()
    print_room_actions()

# Main game loop
running = True
while running:
    player_input = input("\n> ")
    # player_input = get_next_action(shortest_knowing)

    match player_input.lower():
        case "look out the window":
            current_room = 1
            print()
            print_room_descriptions()
            print_room_actions()
        case "look in the closet":
            current_room = 2
            print()
            print_room_descriptions()
            print_room_actions()
        case "take the jacket":
            current_room = 3
            print()
            print_room_descriptions()
            inventory.append("JACKET")
            print(">>> JACKET has been added to your inventory.\n")
            print_room_actions()
        case "search the jacket":
            current_room = 4
            print()
            print_room_descriptions()
            print_room_actions()
        case "head out the room":
            current_room = 5
            state = 1
            print()
            print_room_descriptions()
            print_room_actions()

        # Go back to the starting room if you want
        case "go back to the room":
            current_room = 0
            print()
            print_room_actions()
        # Go back to the hallway
        case "go back to the hallway":
            current_room = 5
            print()
            print_room_actions()
        case "open the door on the right":
            current_room = 6
            print()
            print_room_descriptions()
            print_room_actions()
        case "search the bathroom":
            current_room = 7
            print()
            print_room_descriptions()
            print_room_actions()
        case "open the door on the left":
            current_room = 8
            print()
            print_room_descriptions()
            print_room_actions()
        case "search the office":
            current_room = 9
            print()
            print_room_descriptions()
            print_room_actions()
        case "yes":
            # Case for "Search the office, take the burned picture?"
            if current_room == 9:
                current_room = 10
                print()
                inventory.append("1/3 OF BURNED PHOTO")
                print(">>> 1/3 OF BURNED PHOTO has been added to your inventory.\n\n")
                print_room_descriptions()
                print_room_actions()
            # Case for "Explore downtown, take the newspaper article?"
            elif current_room == 17:
                current_room = 18
                print()
                inventory.append("NEWSPAPER ARTICLE")
                print(">>> NEWSPAPER ARTICLE has been added to your inventory.\n\n")
                print_room_descriptions()
                print_room_actions()
            # Case for "Go to the church, go into the church?"
            elif current_room == 20:
                current_room = 21
                print()
                print_room_descriptions()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    text = church_have_items["have"]
                    print_list(text)
                else:
                    text = church_have_items["have not"]
                    print_list(text)
                # Start of ACT 2, THE RED CHAPEL
                current_room = 23
                print()
                print_room_descriptions()
                print_room_actions()
            else:
                break
        case "no":
            # Case for "Search the office, take the burned picture?"
            if current_room == 9:
                current_room = 11
                print()
                print_room_descriptions()
                print_room_actions()
            # Case for "Explore downtown, take the newspaper article?"
            elif current_room == 17:
                current_room = 19
                print()
                print_room_descriptions()
                print_room_actions()
            # Case for "Go to the church, go into the church?" But saying no ends the game.
            elif current_room == 20:
                current_room = 22
                print()
                print_room_descriptions()
                running = False
            else:
                break
        case "enter the living room":
            current_room = 12
            print()
            print_room_descriptions()
            print_room_actions()
        # Go back to the living room if you want
        case "go back to the living room":
            current_room = 12
            print()
            print_room_actions()
        case "go to the kitchen":
            current_room = 13
            print()
            print_room_descriptions()
            print_room_actions()
        case "search the kitchen":
            current_room = 14
            print()
            print_room_descriptions()
            print_room_actions()
        case "go to the backyard":
            current_room = 15
            print()
            print_room_descriptions()
            print_room_actions()
        case "head outside and into town":
            current_room = 16
            print()
            print_room_descriptions()
            print_room_actions()

        case "explore the town":
            current_room = 17
            print()
            print_room_descriptions()
            print_room_actions()

        # Take the newspaper article? in previous "yes" and "no" cases.

        case "go back to the town square":
            current_room = 16
            print()
            print_room_actions()
        case "go to the church":
            current_room = 20
            print()
            print_room_descriptions()
            print_room_actions()

        # START OF ACT 1, THE RED CHAPEL
        case "take a break":
            chance = random.random()
            if chance > 0.3:
                current_room = 24
                print()
                print_room_descriptions()
                print_room_actions()
            else:
                current_room = 25
                print()
                print_room_descriptions()
                running = False
        case "enter the church":
            if current_room == 24:
                current_room = 26
                print()
                print_room_descriptions()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    inventory.append("2/3 OF BURNED PHOTO")
                    text = redchapel_have_items["have"]
                    print_list(text)
                else:
                    text = redchapel_have_items["have not"]
                    print_list(text)
                    if "JACKET" in inventory:
                        text = redchapel_have_items["have jacket"]
                        print_list(text)
                    else:
                        text = redchapel_have_items["have not jacket"]
                        print_list(text)
                current_room = 29
                print()
                print_room_descriptions()
                print_room_actions()
            elif current_room == 30:
                current_room = 32
                print()
                print_room_descriptions()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE"
                    and "2/3 OF BURNED PHOTO" in inventory
                ):
                    inventory.append("3/3 OF BURNED PHOTO")
                    text = whitechapel_have_items["have"]
                    print_list(text)
                    print()
                    current_room = 38
                    print_room_actions()
                else:
                    if "JACKET" in inventory:
                        text = whitechapel_have_items["have jacket"]
                        print_list(text)
                    else:
                        text = whitechapel_have_items["have not jacket"]
                        print_list(text)
                    text = whitechapel_have_items["have not"]
                    print_list(text)
                    text = blackchapel_have_items["have not"]
                    print_list(text)
                    current_room = 37
                    print()
                    print_room_descriptions()
                    running = False
        case "wait for an invitation":
            if current_room == 24:
                current_room = 27
                print()
                print_room_descriptions()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    inventory.append("2/3 OF BURNED PHOTO")
                    text = redchapel_have_items["have"]
                    print_list(text)
                else:
                    text = redchapel_have_items["have not"]
                    print_list(text)
                    if "JACKET" in inventory:
                        text = redchapel_have_items["have jacket"]
                        print_list(text)
                    else:
                        text = redchapel_have_items["have not jacket"]
                        print_list(text)
                current_room = 29
                print()
                print_room_descriptions()
                print_room_actions()
            elif current_room == 30:
                current_room = 33
                print()
                print_room_descriptions()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE"
                    and "2/3 OF BURNED PHOTO" in inventory
                ):
                    inventory.append("3/3 OF BURNED PHOTO")
                    text = whitechapel_have_items["have"]
                    print_list(text)
                    print()
                    current_room = 38
                    print_room_actions()
                else:
                    if "JACKET" in inventory:
                        text = whitechapel_have_items["have jacket"]
                        print_list(text)
                    else:
                        text = whitechapel_have_items["have not jacket"]
                        print_list(text)
                    text = whitechapel_have_items["have not"]
                    print_list(text)
                    text = blackchapel_have_items["have not"]
                    print_list(text)
                    current_room = 37
                    print()
                    print_room_descriptions()
                    running = False
        case "turn away":
            if current_room == 24:
                current_room = 28
                print()
                print_room_descriptions()
                running = False
            elif current_room == 29:
                current_room = 34
                print()
                print_room_descriptions()
                running = False

        case "walk forward":
            current_room = 30
            print()
            print_room_descriptions()
            print_room_actions()
        case "turn back around":
            current_room = 31
            print()
            print_room_descriptions()
            running = False
        case "accept your fate":
            text = blackchapel_have_items["have"]
            print_list(text)
            running = False
        case "deny your fate":
            current_room = 35
            print()
            print_room_descriptions()
            running = False

        case "save":
            save_game(current_room, inventory)
            running = False

        case "quit":
            print("Exiting the game now.")
            running = False

        case _:
            print("\n\nUnknown command. Try again.\n\n")
            print_room_actions()

# End CPU monitoring
end_time = time.time()
final_cpu = psutil.cpu_times()
final_process_cpu = psutil.Process().cpu_times()

# Calculate CPU usage
# Calculates the total CPU time available system-wide during the game's execution
total_cpu_time = sum(final_cpu) - sum(initial_cpu)
process_cpu_time = (final_process_cpu.user - initial_process_cpu.user) + (
    final_process_cpu.system - initial_process_cpu.system
)
cpu_usage_percentage = (process_cpu_time / total_cpu_time) * 100

# Print CPU usage and runtime
print("\n\nRUNTIME: %s seconds" % (end_time - start_time))
print(f"Total elapsed time: {end_time - start_time:.2f} seconds")
print(f"CPU time used by script: {process_cpu_time:.2f} seconds")
print(f"Total CPU time available: {total_cpu_time:.2f} seconds")
print(f"CPU usage percentage: {cpu_usage_percentage:.2f}%")
