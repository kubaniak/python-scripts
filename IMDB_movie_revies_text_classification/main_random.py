import json
import numpy as np
import tensorflow as tf
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.preprocessing.sequence import pad_sequences
import random

# Load the IMDB dataset with a vocabulary size of 10,000, and skips the top 10 most common words
vocab_size = 50000
skip_top_words = 0
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size, skip_top=skip_top_words)

# Pad sequences to make them of equal length
max_length = 200
x_train = pad_sequences(x_train, maxlen=max_length)
x_test = pad_sequences(x_test, maxlen=max_length)

# Function to build and compile the model with given hyperparameters
def build_model(embedding_dim, batch_size):
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Hyperparameter tuning settings
num_configs = 5  # Number of different configurations to try
embedding_dim_choices = [8, 16, 32]  # Possible values for embedding_dim
epochs_choices = [3, 5, 7]  # Possible values for epochs
batch_size_choices = [32, 64, 128]  # Possible values for batch_size

# Random search for hyperparameter tuning
models_data = []

for i in range(num_configs):
    # Randomly sample hyperparameters for this configuration
    embedding_dim = random.choice(embedding_dim_choices)
    epochs = random.choice(epochs_choices)
    batch_size = random.choice(batch_size_choices)

    # Build and compile the model with the current hyperparameters
    model = build_model(embedding_dim, batch_size)

    # Train the model and obtain the test accuracy
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)
    _, test_accuracy = model.evaluate(x_test, y_test)

    model_params = {
        'layers': [layer.__class__.__name__ for layer in model.layers],
        'epochs': epochs,
        'batch_size': batch_size,
        'embedding_dim': embedding_dim,
        'vocab_size': vocab_size,
        'skip_top_words': skip_top_words,
        'test_accuracy': test_accuracy
    }

    models_data.append(model_params)

    print(f"Configuration {i+1}/{num_configs} - Test accuracy: {test_accuracy:.4f}")

# Save model parameters to a JSON file
json_file = 'model_parameters.json'

try:
    with open(json_file, 'r') as f:
        existing_models_data = json.load(f)
except FileNotFoundError:
    existing_models_data = []

# Append the new model parameters to the existing data
existing_models_data.extend(models_data)

with open(json_file, 'w') as f:
    json.dump(existing_models_data, f, indent=4)
