from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Function to load words from a file
def load_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words

# Path to your words file
file_path = "D:/Projects/Python/wordle_clone/words_alpha.txt"

# Load words from file
word_list = load_words(file_path)

# Filter six-letter words
six_letter_words = [word.lower() for word in word_list if len(word) == 6 and word.isalpha()]

@app.route('/')
def index():
    # Start a new game
    session['random_word'] = random.choice(six_letter_words)
    session['guesses'] = 0
    session['wrong_letters'] = []
    session['messages'] = []
    session['position_map'] = {i: w for i, w in enumerate(session['random_word'])}
    session['count_letters'] = {w: session['random_word'].count(w) for w in set(session['random_word'])}
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    guess = request.form['guess'].lower()

    if len(guess) != 6:
        session['messages'].append("Your guess needs to be 6 letters")
        return render_template('index.html', messages=session['messages'])

    if guess not in six_letter_words:
        session['messages'].append("Your guess is invalid")
        return render_template('index.html', messages=session['messages'])

    session['guesses'] += 1

    if guess == session['random_word']:
        session['messages'].append(f"<span class='correct'>{guess}</span>")
        session['messages'].append("Congratulations, you got it correct in {} guesses".format(session['guesses']))
        return render_template('index.html', messages=session['messages'])

    guess_mapper = {}
    temp_count_letters = session['count_letters'].copy()
    result = ""

    # First pass to find exact matches
    for j in range(len(guess)):
        if guess[j] == session['random_word'][j]:
            guess_mapper[j] = "G"
            temp_count_letters[guess[j]] -= 1
        else:
            guess_mapper[j] = None

    # Second pass to find partial and wrong matches
    for j in range(len(guess)):
        if guess_mapper[j] is None:
            if guess[j] in temp_count_letters and temp_count_letters[guess[j]] > 0:
                guess_mapper[j] = "Y"
                temp_count_letters[guess[j]] -= 1
            else:
                guess_mapper[j] = "R"
                if guess[j] not in session['wrong_letters']:
                    session['wrong_letters'].append(guess[j])
    
    for j in range(len(guess)):
        if guess_mapper[j] == "G":
            result += f"<span class='correct'>{guess[j]}</span>"
        elif guess_mapper[j] == "Y":
            result += f"<span class='partial'>{guess[j]}</span>"
        else:
            result += f"<span class='wrong'>{guess[j]}</span>"

    wrong_letters_str = ", ".join(session['wrong_letters'])

    session['messages'].append(f"{result}")
    session['messages'].append(f"Wrong letters: {wrong_letters_str}")

    if session['guesses'] >= 6:
        session['messages'].append("Unlucky. The correct word is {}".format(session['random_word']))
        return render_template('index.html', messages=session['messages'])
    return render_template('index.html', messages=session['messages'])

@app.route('/reset', methods=['POST'])
def reset():
    # Clear session and start a new game
    session.clear()
    return index()

if __name__ == '__main__':
    app.run(debug=True)