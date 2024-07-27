#Filename: Advanced ship compression.py

#Player vs AI Battleship game

#Written by Ayush Yajaman, 2024

#Note: I have used the variables row and col in multiple functions but they are localised variable that are pertinent only to the function they are declared in
#Notr: In for loops, I have used variables like 'i' and 'j' because they are mostly just used for iterations

# Importing necessary libraries
import random # To generate random integers and randomly choose elements from a lsit
from termcolor import colored #To display coloured text for more immersive user experience
import time #To add delay between different parts of the game

# Instruction for the game
print(colored("You will be playing a game of battleship against an AI. It is extremely smart so you have to bring out your best game!",'magenta'))
print(colored("NOTE: The code is designed cleverly to not error out even if you doesn't adhere to the instructions so you can start playing without reading the rules and learn as you play!",'magenta'))
print(colored("But if you are keen on the rules, here they are:",'magenta'))
print(colored("-> Ship with 2 holes = Destroyer     Ships with 3 holes = Submarine and Cruiser      Ships with 4 holes = Battleship     Ships with 5 holes: Carrier",'magenta'))
print(colored("-> Coordinates should be inputted in the following form: 1a, 10j. The number should come first and then the letter. Capitalization doesn't matter!",'magenta'))
print(colored("-> You will be asked to first place your ships. You can visualise the coordinateds by looking at the player board. You will be asked to place 5 different ships: Destroyer, Submarine, Cruiser, Battleship and Carrier.",'magenta'))
print(colored("-> IMPORTANT: While placing your ships, make sure that you are placing them either horizontally or vertically and they are within the board. Also, make sure you are not crashing your own ships! Finally, the length of your ship should be the number of holes it has. For example, acceptable are:",'magenta'))
print(colored("     Start coordinate of ship with 2 holes: 1a    End coordinate of ship with 2 holes: 2a",'magenta'))
print(colored("     Start coordinate of ship with 5 holes: 10j    End coordinate of ship with 2 holes: 10f",'magenta'))
print(colored("-> After placing all the ships, the battle begins! The AI starts firing at you and you start firing at AI. Whoever manages to sink all the opponent's ships first wins!",'magenta'))
print(colored("-> Colour Codes:",'magenta'))
print(colored("o -> ",'yellow'), end='')
print(colored("Player's Ship Positions",'magenta'))
print(colored("o -> ",'green'), end='')
print(colored("Player hits an AI Ship",'magenta'))
print(colored("o -> ",'grey'), end='')
print(colored("AI hits a Player Ship",'magenta'))
print(colored("X -> ",'red'), end='')
print(colored("AI or Player has missed",'magenta'))

#Initialising variables
rows = 10
columns = 10
ship_types = [2, 3, 3, 4, 5]
alphabet = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
ai_positions = []
player_positions = []
hit = False
ship_sunk = False
placed_first_ship3 = False
player_ship1 = []
player_ship2 = []
player_ship3 = []
player_ship4 = []
player_ship5 = []
ai_ship1 = []
ai_ship2 = []
ai_ship3 = []
ai_ship4 = []
ai_ship5 = []
already_guessed = []
player_already_guessed = []
ai_damage = []
ai_miss_cross = []
player_miss_cross = []
grey = []

# Print column headers
def column():
    for column_header in alphabet:
        print(column_header, end=' ')

# Add colourised ships that have been hit, ships that are active, AI missed shots and water for player board
def gameboard(positions, type):
    # Print column headers
    print("   ", end= "")
    column()
    print('')    
    line = ""  # Initialize an empty string for each line
    k = 1  # Initialize k to 1 (starting position on the board)    
    # Loop through rows
    for i in range(0, columns):
        # Print row number with appropriate spacing
        if i != 9:
            print(" "+ str(i + 1), end=' ')
        else:
            print(i + 1, end=' ')        
        # Loop through columns
        for j in range(0, 10):
            if type == "ai":
            #If player has correctly guessed that position
                if k in ai_damage:
                    line = line + colored("o ", 'green')
                # Check if position k is marked as a missed shot by player
                elif k in player_miss_cross:
                    line = line + colored("X ",'red')
                else:
                    # Print water if position is not fired upon by playrt
                    line = line + colored("* ", 'light_blue')
            elif type == "player":
                #If the position has not yet been guessed by AI and player's ship is on that position
                if k in positions:
                    line = line + colored("o ", 'yellow')
                # Check if position is a missed shot by AI
                elif k in ai_miss_cross:
                    line = line + colored("X ",'red')
                # Check if position is hit by AI correctly
                elif k in grey:
                    line = line + colored("o ",'grey' )
                #If position has not yet been guessed by AI and player's ship is not in that position
                else:
                    line = line + colored("* ", 'light_blue')
            k = k + 1  # Move to the next position           
        print(line)  # Print the line for the current row
        line = ""  # Reset line for the next row
    if type == "ai":
        print("        AI Board        ")  # Print a label for the AI's board
    elif type == "player":
        print("      Player Board        ") # Print a label for the player's board

#Divider to distinguish between AI and player board
def divider():
    print("-------------------")

#Generating game board
def generate_game_board():
    return [["* " for i in range(columns)] for j in range(rows)] #Creates a 10 by 10 board (columns and rows = 10)

# Checks to see if AI's ships are colliding with each other or not
def check_collision(board, coordinates, ship_type):
    for coord in coordinates:
        row, col = coord
        if board[row][col] != "* ": #Checks to see if that position is NOT water
            return True
    return False

# Return True or False if AI ships collision detected
def ai_check_collision(board, row, col, direction, ship_type):
    if direction == "right":
        return any(board[row][col + i] != "* " for i in range(ship_type)) # Check each cell to the right as far as the ship's length
    elif direction == "left":
        return any(board[row][col - i] != "* " for i in range(ship_type)) # Check each cell to the left as far as the ship's length
    elif direction == "down":
        return any(board[row + i][col] != "* " for i in range(ship_type)) # Check each cell downward as far as the ship's length
    elif direction == "up":
        return any(board[row - i][col] != "* " for i in range(ship_type)) # Check each cell upward as far as the ship's length

# Appends values of individual ships to corresponding lists
def appender(ship_type, ai_ship_coord):
    if ship_type == 2:
        ai_ship1.append(ai_ship_coord)
    elif ship_type == 3:
        if len(ai_ship2) < 3:
            ai_ship2.append(ai_ship_coord)
        else:
            ai_ship3.append(ai_ship_coord)
    elif ship_type == 4:
        ai_ship4.append(ai_ship_coord)
    elif ship_type == 5:
        ai_ship5.append(ai_ship_coord)

#Place AI ships on board without overlap or without it going out of board
def ai_place_ship(board, ship_type):
    # Loop until a valid ship placement is found
    while True:
        # Randomly choose a direction
        direction = random.choice(["right", "up", "down", "left"])
        
        # Randomly generate row and column indices based on direction and ship size
        if direction == "right":
            row = random.randint(0, rows - 1)
            col = random.randint(0, columns - ship_type)
        elif direction == "left":
            row = random.randint(0, rows - 1)
            col = random.randint(ship_type - 1, columns - 1)
        elif direction == "down":
            col = random.randint(0, columns - 1)
            row = random.randint(0, rows - ship_type)
        elif direction == "up":
            col = random.randint(0, columns - 1)
            row = random.randint(ship_type - 1, rows - 1)

        # Check for collision with existing ships
        if not ai_check_collision(board, row, col, direction, ship_type):
            # Place the ship on the board and update positions and data
            if direction == "right":
                for i in range(ship_type):
                    board[row][col + i] = colored("o ", 'red') #note: This won't be seen in the actual game ever. I had done this to help me visualise while programming.
                    ai_positions.append(row * columns + col + i + 1) #Converting row and column to one number
                    appender(ship_type, row * columns + col + i + 1) #Calling appender function to append  coordinates to respective lists
            elif direction == "left":
                for i in range(ship_type):
                    board[row][col - i] = colored("o ", 'red') #note: This won't be seen in the actual game ever. I had done this to help me visualise while programming.
                    ai_positions.append(row * columns + col - i + 1) #Converting row and column to one number
                    appender(ship_type, row * columns + col - i + 1) #Calling appender function to append  coordinates to respective lists
            elif direction == "down":
                for i in range(ship_type):
                    board[row + i][col] = colored("o ", 'red') #note: This won't be seen in the actual game ever. I had done this to help me visualise while programming.
                    ai_positions.append((row + i) * columns + col + 1) #Converting row and column to one number
                    appender(ship_type, (row + i) * columns + col + 1)#Calling appender function to append  coordinates to respective lists
            elif direction == "up":
                for i in range(ship_type):
                    board[row - i][col] = colored("o ", 'red') #note: This won't be seen in the actual game ever. I had done this to help me visualise while programming.
                    ai_positions.append((row - i) * columns + col + 1) #Converting row and column to one number
                    appender(ship_type, (row - i) * columns + col + 1)#Calling appender function to append  coordinates to respective lists
            # Break the loop once ship is placed
            break

# Takes coordinate input from the user, converts it into a number, and places the ship appropriately on the board.
def place_ship(board, ship_type):
    global placed_first_ship3  # Used to track whether the first ship of type 3 has been placed
    coordinates = []  # List to store coordinates of the ship
    while True:
        # Get start and end coordinates from the user and convert them into numerical format
        start_coord = conversion(f"Enter start coordinate for ship with {ship_type} holes: ") #Returns a tuple
        end_coord = conversion(f"Enter end coordinate for ship with {ship_type} holes: ") #Returns a tuple
        if start_coord is not None and end_coord is not None:
            # Call get_coordinates function to fill in middle part
            coordinates = get_coordinates(start_coord, end_coord)
            # Check if the coordinates are valid for placing the ship
            if len(coordinates) == ship_type and not check_collision(board, coordinates, ship_type):
                # Place the ship on the board and update positions and ship lists
                for coord in coordinates:
                    row, col = coord
                    board[row][col] = colored("o ", 'yellow')
                    player_positions.append(row * columns + col + 1)
                    # Update ship lists based on ship type
                    if ship_type == 2:
                        player_ship1.append(row * columns + col + 1)
                    elif ship_type == 3:
                        if not placed_first_ship3:
                            player_ship2.append(row * columns + col + 1)
                            if len(player_ship2) == 3:
                                placed_first_ship3 = True
                        else:
                            player_ship3.append(row * columns + col + 1)
                    elif ship_type == 4:
                        player_ship4.append(row * columns + col + 1)
                    elif ship_type == 5:
                        player_ship5.append(row * columns + col + 1)
                # Display the updated game board, divider, and break out of the loop
                gameboard(player_positions, "player")
                divider()
                break
            else:
                print("Invalid ship placement! Make sure your ship is of the right length, within the board, and not overlapping with other ships.")
        else:
            print("Invalid coordinates! Please enter coordinates in the format '1a' to '10j'.")

#Converts integer to the coordinate form (1a to 10j)    
def convert_to_grid_format(number):
    row = (number - 1) // 10 + 1  # Calculate the row number
    col = chr(((number - 1) % 10) + 97)  # Calculate the column letter using ASCII codes
    return str(row) + col  # Combine row number and column letter

#Converts Raw user coordinate input into number so that it can be placed on board
#It rigorously checks for correct inout and if incorrect input detected, it prompts the user to give correct input
def conversion(question):
    while True:
        input_question = input(question).upper()
        if len(input_question) == 2:
            if input_question[0].isdigit() and input_question[1].isalpha(): # Checks if first character is a digit and second one is an alphabet
                row = int(input_question[0]) - 1 # Convert to 0-based indexing
                col = ord(input_question[1]) - ord('A')  # Convert column letter to 0-based indexing
                if 0 <= row < rows and 0 <= col < columns: #columns and rows here are 10 as initialized before
                    return row, col
                else:
                    print("Invalid coordinates! Please enter coordinates in the format '1a' to '10j'.")
            else:
                print("Invalid coordinates! Please enter coordinates in the format '1a' to '10j'.")
        elif len(input_question) == 3 and input_question[0:2] == '10' and input_question[2].isalpha() and input_question[2] in alphabet:
                row = 9
                col = alphabet[input_question[2]]
                return row, col
        else:
            print("Invalid coordinates! Please enter coordinates in the format '1a' to '10j'.")

#Fills up the middle part automatically when user enters correct input
def get_coordinates(start_coord, end_coord):
    start_row, start_col = start_coord # Unpacking the tuple
    end_row, end_col = end_coord # Unpacking the tuple
    coordinates = []
    if start_row == end_row: #Handles horizontal placement
        for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
            coordinates.append((start_row, col))
    elif start_col == end_col: #Handles vertical placement
        for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
            coordinates.append((row, start_col))
    return coordinates

#Handles turns. Once AI fires, once user fires
def turn_handler():
    smart_ai()
    player_fire()

# First fire of AI (random)
def ai_fire():
    global hit, ship_type
    ai_hit_location = random.randint(1, 100)
    while ai_hit_location in already_guessed: #Makes sure it doesn't guess a location already been guessed
        ai_hit_location = random.randint(1, 100)
    print("AI fires: ", end= "")
    print(convert_to_grid_format(ai_hit_location))
    if ai_hit_location in player_ship1 or ai_hit_location in player_ship2 or ai_hit_location in player_ship3 or ai_hit_location in player_ship4 or ai_hit_location in player_ship5:
        time.sleep(1) # To give an effect
        print("Hit!")
        grey.append(ai_hit_location) #Used for marking hit ships
        player_positions.remove(ai_hit_location)
        if ai_hit_location in player_ship1:
            ship_type = 1 # Used later to destroy this ship type completely
            player_ship1.remove(ai_hit_location)
        elif ai_hit_location in player_ship2:
            ship_type = 2 # Used later to destroy this ship type completely
            player_ship2.remove(ai_hit_location)
        elif ai_hit_location in player_ship3:
            ship_type = 3 # Used later to destroy this ship type completely
            player_ship3.remove(ai_hit_location)
        elif ai_hit_location in player_ship4:
            ship_type = 4 # Used later to destroy this ship type completely
            player_ship4.remove(ai_hit_location)
        elif ai_hit_location in player_ship5:
            ship_type = 5 # Used later to destroy this ship type completely
            player_ship5.remove(ai_hit_location)
        hit = True
    else:
        time.sleep(1)
        print("Miss!")
        ai_miss_cross.append(ai_hit_location) #Used for AI misses
        hit = False
    already_guessed.append(ai_hit_location)

# Player fire logic
def player_fire():
    hit_location = conversion("Where do you want to fire? ") #Converting to fired coordinate to a (x,y) tuple
    while hit_location in player_already_guessed: #Makes sure it doesn't guess a location already been guessed
        print("You've already guessed that location. Please choose a different one.")
        hit_location = conversion("Where do you want to fire? ") #Converting to fired coordinate to a (x,y) tuple
    player_already_guessed.append(hit_location)
    row, col = hit_location #Unpacking the tuple and assigning the respective values
    target_position = row * columns + col + 1 #Conversion from row, col to number
    if target_position in ai_positions:
        time.sleep(1) #Delay to give smoother gameplay
        print("Hit!")
        ai_damage.append(target_position)
        ai_positions.remove(target_position)
        #Removing the coordinate from respective ship
        if  target_position in ai_ship1:
            ai_ship1.remove(target_position)
        elif target_position in ai_ship2:
            ai_ship2.remove(target_position)
        elif target_position in ai_ship3:
            ai_ship3.remove(target_position)
        elif target_position in ai_ship4:
            ai_ship4.remove(target_position)
        elif target_position in ai_ship5:
            ai_ship5.remove(target_position)
    else:
        time.sleep(1) #Delay to give smoother gameplay
        print("Miss!")
        player_miss_cross.append(target_position)

#Subroutine to be called when AI fires
def ai_fire_handler():
    print("AI fires: ", end= "")
    print(convert_to_grid_format(shot))
    print("Hit!")
    grey.append(shot)
    player_positions.remove(shot)
    already_guessed.append(shot)

#Once AI hits, making sure it destroys one ship completely
def smart_ai():
    global ship_sunk, hit, ship_type, shot #Variables not specific to this function only   
    if len(player_ship1) == 0 or len(player_ship2) == 0 or len(player_ship3) == 0 or len(player_ship4) == 0 or len(player_ship5) == 0:
        ship_sunk = True
    else:
        ship_sunk = False    
    # Code logic for later use to check if sunken, which ship is sunken
    if len(player_ship1) == 0:
        player_ship1.append("Destroyed")
    if len(player_ship2) == 0:
        player_ship2.append("Destroyed")
    if len(player_ship3) == 0:
        player_ship3.append("Destroyed")
    if len(player_ship4) == 0:
        player_ship4.append("Destroyed")
    if len(player_ship5) == 0:
        player_ship5.append("Destroyed")

    if hit and not ship_sunk:
        if ship_type == 1 and len(player_ship1) < 2: #Hitting until the whole ship is destroyed
            shot = random.choice(player_ship1)
            player_ship1.remove(shot)
            ai_fire_handler()
        elif ship_type == 2 and len(player_ship2) < 3: #Hitting until the whole ship is destroyed
            shot = random.choice(player_ship2)
            player_ship2.remove(shot)
            ai_fire_handler()
        elif ship_type == 3 and len(player_ship3) < 3: #Hitting until the whole ship is destroyed
            shot = random.choice(player_ship3)
            player_ship3.remove(shot)
            ai_fire_handler()
        elif ship_type == 4 and len(player_ship4) < 4: #Hitting until the whole ship is destroyed
            shot = random.choice(player_ship4)
            player_ship4.remove(shot)
            ai_fire_handler()
        elif ship_type == 5 and len(player_ship5) < 5: #Hitting until the whole ship is destroyed
            shot = random.choice(player_ship5)
            player_ship5.remove(shot)
            ai_fire_handler()
    else:
        ai_fire()

# Check which ships have been sunk
def ship_type_sunk(ai_or_player):
    if  ai_or_player == "ai": #Checking for AI's ships being sunk
        if len(ai_ship1) == 0:
            print(colored("Destroyer (2 holes) sunken", 'green'))
        if len(ai_ship2) == 0:
            print(colored("Submarine (3 holes) sunken", 'green'))
        if len(ai_ship3) == 0:
            print(colored("Cruiser (3 holes) sunken", 'green'))
        if len(ai_ship4) == 0:
            print(colored("Battleship (4 holes) sunken", 'green'))
        if len(ai_ship5) == 0:
            print(colored("Carrier(5 holes) sunken", 'green'))
    elif ai_or_player == "player": #Checking for player's ships being sunk
        if "Destroyed" in player_ship1 or len(player_ship1) == 0:
            print(colored("Destroyer (2 holes) sunken", 'yellow'))
        if "Destroyed" in player_ship2 or len(player_ship2) == 0:
            print(colored("Submarine (3 holes) sunken", 'yellow'))
        if "Destroyed" in player_ship3 or len(player_ship3) == 0:
            print(colored("Cruiser (3 holes) sunken", 'yellow'))
        if "Destroyed" in player_ship4 or len(player_ship4) == 0:
            print(colored("Battleship (4 holes) sunken", 'yellow'))
        if "Destroyed" in player_ship5 or len(player_ship5) == 0:
            print(colored("Carrier (4 holes) sunken", 'yellow'))

#Main  Game Loop - Runs until every ship is destroyed of AI or player
def main_loop():
        turn_handler() # Handles AI and player turns
        time.sleep(1) #Delay for smoother gameplay
        gameboard(ai_positions, "ai") #Prints AI  game board
        ship_type_sunk("ai") #Prints shunken ships of AI if any
        divider()
        gameboard(player_positions, "player") #Prints Player  game board
        ship_type_sunk("player") #Prints shunken ships of player if any
        print("") #For neater presentation

#Displaying the player board
gameboard(player_positions, "player")

#Displaying the AI's board with battleships (To the user this would just be water)
board = generate_game_board()
for ai_ship_type in ship_types:
    ai_place_ship(board, ai_ship_type)

divider()

#Displaying the player's board with battleships
playerBoard = generate_game_board()
for ship_type in ship_types:
    place_ship(playerBoard, ship_type)

#Indicate the firing phase of the game
print(colored("Prepare for battle! Let the firing begin! Fire at coordinates in the AI Board and see if you can knock some ships down!", 'magenta'))
gameboard(ai_positions, "ai")
print("")

#Run the main game loop until all ships of either AI or player are destroyed
while len(player_positions)!=0 and len(ai_positions)!=0:
    main_loop()

#Check who won the game
if  len(player_positions)==0:
    print(colored("Uh Oh! You lost to AI! Play again and redeem yourself!",'magenta'))
elif len(ai_positions)==0:
    print(colored("You Win! You are better than AI!",'magenta'))
else:
    print(colored("It's a Draw! that was close! You're as good as AI! Play again and try to win!",'magenta'))