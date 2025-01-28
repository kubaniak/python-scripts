import json
from itertools import permutations
import requests
from bs4 import BeautifulSoup
import time

def load_dictionary(file_path="words_dictionary.json"):
    """
    Load the English words dictionary from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing the dictionary.

    Returns:
        set: A set of English words.
    """
    with open(file_path, "r") as file:
        dictionary = json.load(file)
    return set(dictionary)

def is_english_word(word, dictionary):
    """
    Check if a given word is an English word.

    Args:
        word (str): The word to check.
        dictionary (set): A set of English words.

    Returns:
        bool: True if the word is an English word, False otherwise.
    """
    return word in dictionary

def generate_permutations(strings, dictionary):
    """
    Generate all permutations of the given strings and filter English words.

    Args:
        strings (list): A list of strings.
        dictionary (set): A set of English words.

    Returns:
        list: A list of all English permutations of the given strings.
    """
    for r in range(2, 5):  # Length of permutations from 2 to 4
        for perm in permutations(strings, r):
            perm_word = ''.join(perm)
            if is_english_word(perm_word, dictionary):
                yield perm_word

def save_permutations_to_file(permutations, file_path="permutations.txt"):
    """
    Save all permutations to a file.

    Args:
        permutations (iterable): An iterable of permutations.
        file_path (str): Path to the file where permutations will be saved.

    Returns:
        None
    """
    with open(file_path, "w") as file:
        file.writelines(f"{perm}\n" for perm in permutations)
    print("Permutations saved to permutations.txt")

def get_input_strings(url="https://combinations.org/"):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        soup.prettify()
        print(soup)
        elements = soup.find_all("wordpiece_label")
        print(elements)
        input_strings = [element.text for element in elements]
        return input_strings
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []


if __name__ == "__main__":
    input_strings = ["es", "ed", "am", "sh", "us", "cla", "te", "ck", "tax", "du", "ens", "por"]

    # Load the dictionary once
    dictionary = load_dictionary()
    
    # Generate and save English permutations
    english_permutations = list(generate_permutations(input_strings, dictionary))
    print("Total English Permutations:", len(english_permutations))
    save_permutations_to_file(english_permutations)
    
    # Print English permutations
    print("Permutations in English language:")
    for perm in english_permutations:
        print(perm)
    print("Found Words:", len(english_permutations))
