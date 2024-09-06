import random
import time
import requests

# Dictionary mapping each letter to its Scrabble point value
LETTER_VALUES = {
    'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1, 'L': 1, 'N': 1, 'R': 1, 'S': 1, 'T': 1,
    'D': 2, 'G': 2,
    'B': 3, 'C': 3, 'M': 3, 'P': 3,
    'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
    'K': 5,
    'J': 8, 'X': 8,
    'Q': 10, 'Z': 10
}


def calculate_score(word):
    """
    Calculate the Scrabble score for a given word.

    Args:
    word (str): The word to score.

    Returns:
    int: The total score for the word.
    """
    return sum(LETTER_VALUES.get(char.upper(), 0) for char in word)


def is_valid_word(word):
    """
    Check if a word is valid using an online dictionary API.

    Args:
    word (str): The word to validate.

    Returns:
    bool: True if the word is valid, False otherwise.
    """
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url, timeout=5)  # Timeout after 5 seconds
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error checking word validity: {e}")
        return False


def play_round(word=None):
    """
    Play a single round of the word game.

    Args:
    word (str, optional): A pre-defined word for testing purposes.

    Returns:
    int: The score for this round.
    """
    start_time = time.time()

    while True:
        # Check if time limit (15 seconds) has been exceeded
        if time.time() - start_time > 15:
            print("Time's up!")
            return 0

        # If a word is provided (for testing), use it; otherwise, prompt the user
        if word is not None:
            required_length = random.randint(3, 10)
            print(f"Enter a word with {required_length} letters. You have 15 seconds.")
            if len(word) != required_length:
                print(f"The word must be {required_length} letters long.")
                continue
        else:
            word = input("Your word: ").strip()

        # Validate input: must be alphabetic characters only
        if not word.isalpha():
            print("Please enter only alphabetic characters.")
            continue

        # Check if the word is valid using the dictionary API
        if not is_valid_word(word):
            print("That's not a valid word. Please try again.")
            continue

        break

    # Calculate scores
    time_taken = time.time() - start_time
    base_score = calculate_score(word)
    time_bonus = max(0, int((15 - time_taken) * 2))  # 2 points per second remaining
    total_score = base_score + time_bonus

    # Display round results
    print(f"Word: {word}")
    print(f"Base score: {base_score}")
    print(f"Time bonus: {time_bonus}")
    print(f"Total score: {total_score}")

    return total_score


def play_game():
    """
    Main game loop. Plays up to 10 rounds or until the player quits.
    """
    total_score = 0
    rounds_played = 0

    while rounds_played < 10:
        print(f"\nRound {rounds_played + 1}")
        round_score = play_round()
        total_score += round_score
        rounds_played += 1

        if rounds_played < 10:
            play_again = input("Press Enter to play another round, or 'q' to quit: ")
            if play_again.lower() == 'q':
                break

    print(f"\nGame over! Your total score is: {total_score}")


if __name__ == "__main__":
    play_game()