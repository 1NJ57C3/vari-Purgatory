import os

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
