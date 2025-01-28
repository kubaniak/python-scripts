import nltk
from itertools import permutations

# Download the NLTK word list if not already downloaded
nltk.download('words')

# Load the English words corpus
english_words = set(nltk.corpus.words.words())

def is_english_word(word):
    """
    Check if a given word is an English word.

    Args:
        word (str): The word to check.

    Returns:
        bool: True if the word is an English word, False otherwise.
    """
    return word.lower() in english_words

def generate_permutations(strings):
    """
    Generate all permutations of the given strings.

    Args:
        strings (list): A list of strings.

    Returns:
        list: A list of all permutations of the given strings.
    """
    permutations_list = []
    for r in range(2, 5):  # Length of permutations from 2 to 4
        for perm in permutations(strings, r):
            permutations_list.append(''.join(perm))
    return permutations_list

def save_permutations_to_file(permutations):
    """
    Save all permutations to a file.

    Args:
        permutations (list): A list of permutations.

    Returns:
        None
    """
    with open("permutations.txt", "w") as file:
        for perm in permutations:
            file.write(perm + "\n")
    print("Permutations saved to permutations.txt")

if __name__ == "__main__":
    input_strings = ["con", "end", "ous", "par", "ic", "es", "te", "rs", "ho", "no", "ma", "se"]  # Example list of strings
    all_permutations = generate_permutations(input_strings)
    
    print("Total Permutations:", len(all_permutations))

    # Save permutations to a file
    save_permutations_to_file(all_permutations)

    # Apply language filter
    english_permutations = list(filter(is_english_word, all_permutations))
    
    # Print English permutations
    print("Permutations in English language:")
    for perm in english_permutations:
        print(perm)
    print("Found Words:", len(english_permutations))
