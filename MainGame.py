import random
import time
import psutil
import os

from data.rooms import rooms
from data.items import church_have_items, redchapel_have_items, whitechapel_have_items, blackchapel_have_items
from data.knowings import shortest_knowing, technical_shortest, longest_knowing

from utils.help import print_instructions

def get_next_action(sequence):
    if sequence:
        return sequence.pop(0)
    else:
        return "quit"


current_room = 0
inventory = []


def create_save():
    save_file_name = input("What is the name of your saved file? ")
    save_file = open(save_file_name + ".txt", "w")
    save_file.write(str(current_room) + "\n")
    for i in range(len(inventory)):
        save_file.write(inventory[i] + "\n")
    print("Save file: '", save_file_name, "' successfully created.")
    save_file.close()


def load_game():
    validation = True
    while validation:
        load_file_name = input("What is the name of your saved file? ")
        path = "./" + load_file_name + ".txt"
        if os.path.isfile(path):
            load_file = open(load_file_name + ".txt", "r")
            global current_room
            current_room = int(load_file.readline())
            global inventory
            inventory = load_file.read().splitlines()
            print("Save file: '", load_file_name, "' successfully loaded.\n\n")
            load_file.close()
            validation = False
        else:
            print(
                "That file doesn't exist or cannot be found. Do you wish to try again? Y/N\n\n"
            )
            while True:
                again = input("> ")
                if again.lower() == "n":
                    validation = False
                    False
                elif again.lower() == "y":
                    validation = True
                    False
                else:
                    print("Unknown command. Try again.\n\n")


def getDesc(room):
    return room[current_room]["description"]


def getActions(room):
    for x in range(len(room[current_room]["actions"])):
        print("- ", room[current_room]["actions"][x])


def print_split_text():
    desc = getDesc(rooms)
    split_text = desc.split("\n\n")
    for x in range(len(split_text)):
        print(split_text[x])
        input()


def print_list(list):
    for x in range(len(list)):
        print(list[x])
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
    print_split_text()
    getActions(rooms)
else:
    # Starting room
    print_split_text()
    getActions(rooms)

# Main game loop
running = True
while running:
    player_input = input("\n> ")
    # player_input = get_next_action(shortest_knowing)

    match player_input.lower():
        case "look out the window":
            current_room = 1
            print()
            print_split_text()
            getActions(rooms)
        case "look in the closet":
            current_room = 2
            print()
            print_split_text()
            getActions(rooms)
        case "take the jacket":
            current_room = 3
            print()
            print_split_text()
            inventory.append("JACKET")
            print(">>> JACKET has been added to your inventory.\n")
            getActions(rooms)
        case "search the jacket":
            current_room = 4
            print()
            print_split_text()
            getActions(rooms)
        case "head out the room":
            current_room = 5
            state = 1
            print()
            print_split_text()
            getActions(rooms)

        # Go back to the starting room if you want
        case "go back to the room":
            current_room = 0
            print()
            getActions(rooms)
        # Go back to the hallway
        case "go back to the hallway":
            current_room = 5
            print()
            getActions(rooms)
        case "open the door on the right":
            current_room = 6
            print()
            print_split_text()
            getActions(rooms)
        case "search the bathroom":
            current_room = 7
            print()
            print_split_text()
            getActions(rooms)
        case "open the door on the left":
            current_room = 8
            print()
            print_split_text()
            getActions(rooms)
        case "search the office":
            current_room = 9
            print()
            print_split_text()
            getActions(rooms)
        case "yes":
            # Case for "Search the office, take the burned picture?"
            if current_room == 9:
                current_room = 10
                print()
                inventory.append("1/3 OF BURNED PHOTO")
                print(">>> 1/3 OF BURNED PHOTO has been added to your inventory.\n\n")
                print_split_text()
                getActions(rooms)
            # Case for "Explore downtown, take the newspaper article?"
            elif current_room == 17:
                current_room = 18
                print()
                inventory.append("NEWSPAPER ARTICLE")
                print(">>> NEWSPAPER ARTICLE has been added to your inventory.\n\n")
                print_split_text()
                getActions(rooms)
            # Case for "Go to the church, go into the church?"
            elif current_room == 20:
                current_room = 21
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    text = church_have_items["have"].split("\n\n")
                    print_list(text)
                else:
                    text = church_have_items["have not"].split("\n\n")
                    print_list(text)
                # Start of ACT 2, THE RED CHAPEL
                current_room = 23
                print()
                print_split_text()
                getActions(rooms)
            else:
                break
        case "no":
            # Case for "Search the office, take the burned picture?"
            if current_room == 9:
                current_room = 11
                print()
                print_split_text()
                getActions(rooms)
            # Case for "Explore downtown, take the newspaper article?"
            elif current_room == 17:
                current_room = 19
                print()
                print_split_text()
                getActions(rooms)
            # Case for "Go to the church, go into the church?" But saying no ends the game.
            elif current_room == 20:
                current_room = 22
                print()
                print_split_text()
                running = False
            else:
                break
        case "enter the living room":
            current_room = 12
            print()
            print_split_text()
            getActions(rooms)
        # Go back to the living room if you want
        case "go back to the living room":
            current_room = 12
            print()
            getActions(rooms)
        case "go to the kitchen":
            current_room = 13
            print()
            print_split_text()
            getActions(rooms)
        case "search the kitchen":
            current_room = 14
            print()
            print_split_text()
            getActions(rooms)
        case "go to the backyard":
            current_room = 15
            print()
            print_split_text()
            getActions(rooms)
        case "head outside and into town":
            current_room = 16
            print()
            print_split_text()
            getActions(rooms)

        case "explore the town":
            current_room = 17
            print()
            print_split_text()
            getActions(rooms)

        # Take the newspaper article? in previous "yes" and "no" cases.

        case "go back to the town square":
            current_room = 16
            print()
            getActions(rooms)
        case "go to the church":
            current_room = 20
            print()
            print_split_text()
            getActions(rooms)

        # START OF ACT 1, THE RED CHAPEL
        case "take a break":
            chance = random.random()
            if chance > 0.3:
                current_room = 24
                print()
                print_split_text()
                getActions(rooms)
            else:
                current_room = 25
                print()
                print_split_text()
                running = False
        case "enter the church":
            if current_room == 24:
                current_room = 26
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    inventory.append("2/3 OF BURNED PHOTO")
                    text = redchapel_have_items["have"].split("\n\n")
                    print_list(text)
                else:
                    text = redchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    if "JACKET" in inventory:
                        text = redchapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = redchapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                current_room = 29
                print()
                print_split_text()
                getActions(rooms)
            elif current_room == 30:
                current_room = 32
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE"
                    and "2/3 OF BURNED PHOTO" in inventory
                ):
                    inventory.append("3/3 OF BURNED PHOTO")
                    text = whitechapel_have_items["have"].split("\n\n")
                    print_list(text)
                    print()
                    current_room = 38
                    getActions(rooms)
                else:
                    if "JACKET" in inventory:
                        text = whitechapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = whitechapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                    text = whitechapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    text = blackchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    current_room = 37
                    print()
                    print_split_text()
                    running = False
        case "wait for an invitation":
            if current_room == 24:
                current_room = 27
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE" in inventory
                ):
                    inventory.append("2/3 OF BURNED PHOTO")
                    text = redchapel_have_items["have"].split("\n\n")
                    print_list(text)
                else:
                    text = redchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    if "JACKET" in inventory:
                        text = redchapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = redchapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                current_room = 29
                print()
                print_split_text()
                getActions(rooms)
            elif current_room == 30:
                current_room = 33
                print()
                print_split_text()
                if (
                    "JACKET"
                    and "1/3 OF BURNED PHOTO"
                    and "NEWSPAPER ARTICLE"
                    and "2/3 OF BURNED PHOTO" in inventory
                ):
                    inventory.append("3/3 OF BURNED PHOTO")
                    text = whitechapel_have_items["have"].split("\n\n")
                    print_list(text)
                    print()
                    current_room = 38
                    getActions(rooms)
                else:
                    if "JACKET" in inventory:
                        text = whitechapel_have_items["have jacket"].split("\n\n")
                        print_list(text)
                    else:
                        text = whitechapel_have_items["have not jacket"].split("\n\n")
                        print_list(text)
                    text = whitechapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    text = blackchapel_have_items["have not"].split("\n\n")
                    print_list(text)
                    current_room = 37
                    print()
                    print_split_text()
                    running = False
        case "turn away":
            if current_room == 24:
                current_room = 28
                print()
                print_split_text()
                running = False
            elif current_room == 29:
                current_room = 34
                print()
                print_split_text()
                running = False

        case "walk forward":
            current_room = 30
            print()
            print_split_text()
            getActions(rooms)
        case "turn back around":
            current_room = 31
            print()
            print_split_text()
            running = False
        case "accept your fate":
            text = blackchapel_have_items["have"].split("\n\n")
            print_list(text)
            running = False
        case "deny your fate":
            current_room = 35
            print()
            print_split_text()
            running = False

        case "save":
            create_save()
            running = False

        case "quit":
            print("Exiting the game now.")
            running = False

        case _:
            print("\n\nUnknown command. Try again.\n\n")
            getActions(rooms)

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
