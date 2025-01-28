import tensorflow as tf
from keras import layers, models, datasets
import matplotlib.pyplot as plt
import numpy as np

# Load the CIFAR-10 dataset
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# Normalize pixel values to range [0, 1]
train_images, test_images = train_images / 255.0, test_images / 255.0

# Define the class names for visualization
class_names = [
    'Airplane', 'Automobile', 'Bird', 'Cat', 'Deer',
    'Dog', 'Frog', 'Horse', 'Ship', 'Truck'
]

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='tanh', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='tanh'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='tanh'),
    layers.Flatten(),
    layers.Dense(64, activation='sigmoid'),
    layers.Dense(10)
])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model
history = model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))

def plot_training_history(history):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

# Visualize training history
plot_training_history(history)

# Evaluate the model on test data
test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=2)
print(f'Test accuracy: {test_accuracy:.4f}')

# Function to display sample predictions
def plot_sample_predictions(images, labels, predictions):
    plt.figure(figsize=(10, 10))
    for i in range(25):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(images[i])
        predicted_label = np.argmax(predictions[i])
        true_label = labels[i][0]
        color = 'green' if predicted_label == true_label else 'red'
        plt.xlabel("{} ({})".format(class_names[predicted_label], class_names[true_label]), color=color)
    plt.show()

# Get model predictions on test data
predictions = model.predict(test_images)

# Display sample predictions
plot_sample_predictions(test_images, test_labels, predictions)

# Visualization of the activations in the first hidden layer
def visualize_activations(image, model, layer_index):
    model_extract = tf.keras.Model(inputs=model.input, outputs=model.layers[layer_index].output)
    activations = model_extract.predict(np.expand_dims(image, axis=0))

    plt.figure(figsize=(10, 10))
    for i in range(32):
        plt.subplot(4, 8, i + 1)
        plt.imshow(activations[0, :, :, i], cmap='viridis')
        plt.axis('off')
    plt.show()

# Choose an example image from the test set for visualization
example_image_index = 0
example_image = test_images[example_image_index]

# Visualize activations in the first convolutional layer (layer_index=0)
visualize_activations(example_image, model, layer_index=0)
