from pathlib import Path
import random

def build_trie(word_list) -> dict:
    # Realize words as prefix tree (Trie). Time: O(N*L)=O(number_of_words * word_length)
    # Optimize performance for later prefix checks and next letter retrieval as O(L).
    trie = {}
    for word in word_list:
        current_node = trie
        for char in word:
            if char not in current_node:
                current_node[char] = {}
            current_node = current_node[char]
    return trie

def prefix_exists(trie, prefix) -> bool:
    # Checks if a prefix exists in the Trie. Time: O(L).
    current_node = trie
    for char in prefix:
        if char not in current_node:
            return False
        current_node = current_node[char]
    return True

def get_valid_next_letters(trie, prefix) -> list:
    # Returns characters that can continue the prefix. Time: O(L). 
    current_node = trie
    for char in prefix:
        if char not in current_node:
            return []
        current_node = current_node[char]
    return list(current_node.keys())

# Game introduction
print("Welcome to the Letter Game!"
      "\nYou and the computer will take turns picking letters from 'a' to 'z'."
      "\nThe computer always picks a random letter in the easy mode, and a strategic one in the hard mode."
      "\nThe goal is to keep picking letters so that a valid English word starts with the letters picked so far."
      "\nThe game will end when no more valid words can be formed, and the other player wins."
      "\nLet's see who can win the most games!"
      "\n")

# Dictionary selection
dict_choice = input("Please choose a dictionary (1 for standard, 2 for common): ").strip()
while dict_choice not in ["1", "2"]:
    print("Invalid input. Please enter '1' or '2'.")
    dict_choice = input("Please choose a dictionary (1 for standard, 2 for common): ").strip()

if dict_choice == "1":
    word_file = Path(__file__).with_name("words_alpha.txt")
elif dict_choice == "2":
    word_file = Path(__file__).with_name("enable1_words.txt")

# Load dictionary as list
with word_file.open("r", encoding="utf-8") as f:
    my_dict = [line.strip().lower() for line in f if line.strip()]

# Build Trie from dictionary for O(L) prefix checks and next letter retrieval.
word_trie = build_trie(my_dict)

# Difficulty choice
diff_choice = input("Please choose a difficulty level (1 for easy, 2 for hard): ").strip()
while diff_choice not in ["1", "2"]:
    print("Invalid input. Please enter '1' or '2'.")
    diff_choice = input("Please choose a difficulty level (1 for easy, 2 for hard): ").strip()

player_wins = 0
computer_wins = 0
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Game loop
while True:
    print("\nStarting a new game!")
    word_so_far = ""

    while True:
        # User turn
        user_input = input("Please enter a character: ").strip().lower()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        word_so_far += user_input
        print(f"The letters picked so far: {word_so_far}")

        # Check against Trie if word_so_far is a valid prefix. Time:O(L).
        if not prefix_exists(word_trie, word_so_far):
            print("No words in the dictionary can be formed after your turn. Computer wins!")
            computer_wins += 1
            break

        # Computer turn
        if diff_choice == "1": # Easy mode: random letter
            ran_char = random.choice(alphabet)
        elif diff_choice == "2": # Hard mode: strategic letter
            # Get valid next letters from Trie. Time: O(L).
            valid_letters = get_valid_next_letters(word_trie, word_so_far)
            if valid_letters:
                # Pick random valid letter if exists
                ran_char = random.choice(valid_letters)
            else:
                # Pick random letter if none is valid, and lose
                ran_char = random.choice(alphabet)

        print(f"The computer picked: {ran_char}")
        word_so_far += ran_char
        print(f"The letters picked so far: {word_so_far}")

        # Check against Trie if word_so_far is a valid prefix. Time:O(L).
        if not prefix_exists(word_trie, word_so_far):
            print("No words in the dictionary can be formed after the computer's turn. You win!")
            player_wins += 1
            break
    
    # Ask for replay
    while True:
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again in ["y", "n", "yes", "no"]:
            break
        print("Invalid input. Please enter 'yes' or 'no'.")

    if play_again in ["no", "n"]:
        print(f"Thanks for playing! Final score - You: {player_wins}, Computer: {computer_wins}")
        break
    
    print(f"Current score - You: {player_wins}, Computer: {computer_wins}")
