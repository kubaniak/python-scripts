import json
import numpy as np
import tensorflow as tf
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.preprocessing.sequence import pad_sequences
import optuna

# Load the IMDB dataset with a default vocabulary size of 10,000
vocab_size = 10000
skip_top_words = 0
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size, skip_top=skip_top_words)

# Pad sequences to make them of equal length
max_length = 200
x_train = pad_sequences(x_train, maxlen=max_length)
x_test = pad_sequences(x_test, maxlen=max_length)

# Function to build and compile the model with given hyperparameters
def build_model(trial):
    embedding_dim = trial.suggest_categorical('embedding_dim', [4, 8])
    epochs = trial.suggest_int('epochs', 2, 10)
    batch_size = trial.suggest_categorical('batch_size', [16, 32])
    dense_units1 = trial.suggest_categorical('dense_units1', [4, 8])
    dense_units2 = trial.suggest_categorical('dense_units2', [4, 8])
    activation = trial.suggest_categorical('activation', ['softmax'])
    

    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(dense_units1, activation=activation))
    model.add(Dense(dense_units2, activation=activation))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model, embedding_dim, epochs, batch_size, dense_units1, dense_units2, activation

# Optuna hyperparameter tuning
def objective(trial):
    model, embedding_dim, epochs, batch_size, dense_units1, dense_units2, activation = build_model(trial)

    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, use_multiprocessing=True)
    _, test_accuracy = model.evaluate(x_test, y_test)

    return test_accuracy

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=10, show_progress_bar=True)

best_params = study.best_params
best_test_accuracy = study.best_value

print("Best parameters:", best_params)
print("Best test accuracy:", best_test_accuracy)

# Save model parameters to a JSON file
json_file = 'model_parameters_optuna.json'

try:
    with open(json_file, 'r') as f:
        existing_models_data = json.load(f)
except FileNotFoundError:
    existing_models_data = []

model_params = {
    'layers': ['Embedding', 'GlobalAveragePooling1D',
               f"Dense1: {best_params['dense_units1']}, activation: {best_params['activation']}", 
               f"Dense2: {best_params['dense_units2']}, activation: {best_params['activation']}"],
    'vocab_size': vocab_size,
    'embedding_dim': best_params['embedding_dim'],
    'epochs': best_params['epochs'],
    'batch_size': best_params['batch_size'],
    'test_accuracy': best_test_accuracy
}

existing_models_data.append(model_params)

with open(json_file, 'w') as f:
    json.dump(existing_models_data, f, indent=4)
