import random

def load_words(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words
file_path = "D:\Projects\Python\wordle_clone\words_alpha.txt"

word_list = load_words(file_path)
six_letter_words = [word for word in word_list if len(word) == 6 and word.islower()]

# ANSI escape codes for colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

playing = 'y'

while playing == 'y':
    random_word = random.choice(six_letter_words)
    guesses = 0
    correct = False
    position_map = {}
    count_letters = {}
    wrong_letters = set()
    for i, w in enumerate(random_word):
        position_map[i] = w
        count_letters[w] = 1 + count_letters.get(w, 0)
    
    while guesses < 6 and not correct:
        temp_count_letters = count_letters.copy()
        guess = input("Enter 6 letter word to guess\n").lower()
        guess = guess.replace(" ", "")
        
        if len(guess) != 6:
            print("Your guess needs to be 6 letters")
            continue
        if guess not in six_letter_words:
            print("Your guess is invalid")
            continue
        
        guesses += 1
        if guess == random_word:
            correct = True
            print(f"{GREEN}{guess}{RESET}")
            break
        
        guess_mapper = {}
        for j in range(len(guess)):
            if guess[j] == random_word[j]:
                guess_mapper[j] = GREEN + guess[j] + RESET
                temp_count_letters[guess[j]] -= 1
        
        for j in range(len(guess)):
            if j in guess_mapper:
                continue
            if guess[j] in temp_count_letters and temp_count_letters[guess[j]] != 0:
                guess_mapper[j] = YELLOW + guess[j] + RESET
                temp_count_letters[guess[j]] -= 1
            else:
                guess_mapper[j] = RED + guess[j] + RESET
                wrong_letters.add(guess[j])
        
        result = "".join(guess_mapper[j] for j in range(len(guess)))
        print(result)
        print("Wrong letters: ", wrong_letters)
    
    if correct:
        print("Congratulations, you got it correct in", guesses, "guesses")
    else:
        print("Unlucky. The correct word is", random_word)
    
    playing = input("Press y to continue and any other character to exit\n").lower()
