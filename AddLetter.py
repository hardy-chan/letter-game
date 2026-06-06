from pathlib import Path
import random

# load the file to myDict
word_file = Path(__file__).with_name("words_alpha.txt")

with word_file.open("r", encoding="utf-8") as f:
    my_dict = [line.strip() for line in f if line.strip()]
# print(my_dict) # print the list of words in my_dict for testing

print("Welcome to the Letter Game!"
      "\nYou and the computer will take turns picking letters from 'a' to 'z'."
      "\nThe computer always picks a random letter."
      "\nThe goal is to keep picking letters so that a valid English word starts with the letters picked so far."
      "\nThe game will end when no more valid words can be formed, and the other player wins."
      "\nLet's see who can win the most games!")

# initialize player's win count
player_wins = 0
# initialize computer's win count
computer_wins = 0

# game loop
while True:
    print("\nStarting a new game!")
    # initialize the word so far formed by the letters picked
    word_so_far = ""

    # take turns picking letters until the game ends
    while True:
        # ask user to input a character
        user_input = input("Please enter a character: ").strip().lower()
        # check if the user input contains only one character and is a letter
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        word_so_far += user_input

        # print the word so far formed after the user's turn
        print(f"The letters picked so far: {word_so_far}")

        # check if any word in my_dict starts with word_so_far
        if not any(word.startswith(word_so_far) for word in my_dict):
            print("No words in the dictionary can be formed after your turn. Computer wins!")
            computer_wins += 1
            break

        # computer picks random letter from 'a' to 'z' as ranChar
        ranChar = random.choice('abcdefghijklmnopqrstuvwxyz')

        # print the word so far formed
        print(f"The computer picked: {ranChar}")


        word_so_far += ranChar
        # print the word so far formed after the computer's turn
        print(f"The letters picked so far: {word_so_far}")

        # check if any word in my_dict starts with word_so_far
        if not any(word.startswith(word_so_far) for word in my_dict):
            print("No words in the dictionary can be formed after the computer's turn. You win!")
            player_wins += 1
            break
    
    # ask user if they want to play again, get input and check if it's valid
    while True:
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again in ["yes", "no"]:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    if play_again == "no":
        print(f"Thanks for playing! Final score - You: {player_wins}, Computer: {computer_wins}")
        break
    elif play_again == "yes":
        # print current score before starting a new game
        print(f"Current score - You: {player_wins}, Computer: {computer_wins}")
    else:
        # input again if the user input is invalid
        print("Invalid input. Please enter 'yes' or 'no'.")
