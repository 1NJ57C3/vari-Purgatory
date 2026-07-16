def save_game(current_room, inventory):
    save_file_name = input("What is the name of your saved file? ")
    save_file = open(save_file_name + ".txt", "w")
    save_file.write(str(current_room) + "\n")
    for i in range(len(inventory)):
        save_file.write(inventory[i] + "\n")
    print("Save file: '", save_file_name, "' successfully created.")
    save_file.close()
