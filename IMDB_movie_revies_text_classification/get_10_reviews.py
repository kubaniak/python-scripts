import numpy as np
import tensorflow as tf
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.preprocessing.sequence import pad_sequences

# Load the IMDB dataset with a vocabulary size of 10,000, and skips the top 10 most common words
vocab_size = 50000
skip_top_words = 0
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size, skip_top=skip_top_words)

x_combined = np.concatenate((x_train, x_test), axis=0)
y_combined = np.concatenate((y_train, y_test), axis=0)

# Define a dictionary to map word indices to actual words
word_index = imdb.get_word_index()
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# Print the first 10 sentences and their sentiments
print("First 10 Sentences:")
for i in range(10):
    decoded_sentence = ' '.join([reverse_word_index.get(word_index - 3, '?') for word_index in x_combined[i]])
    sentiment = "positive" if y_combined[i] == 1 else "negative"
    print(f"Sentence {i+1}: {decoded_sentence}")
    print(f"Sentiment: {sentiment}\n")