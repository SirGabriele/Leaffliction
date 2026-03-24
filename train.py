import tensorflow as tf
from tensorflow.keras import Sequential, layers

images_folder = "images/"
image_size = (128, 128)
batch_size = 32
shape = (image_size[0], image_size[1], 3)

print("="*50)
print("\nLoading training dataset...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    images_folder,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=image_size,
    batch_size=batch_size
)
print("Training dataset loaded successfully!\n")
print("Loading validation dataset...")

val_ds = tf.keras.utils.image_dataset_from_directory(
    images_folder,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=image_size,
    batch_size=batch_size
)
print("Validation dataset loaded successfully!\n")
print("="*50)

class_names = train_ds.class_names
print("\nClasses détectées :", class_names)


model = Sequential()
model.add(layers.Input(shape))
model.add(layers.Rescaling(1.0 / 255))

model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))

model.add(layers.Dropout(0.5))
model.add(layers.Dense(len(class_names), activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
print("Model compiled successfully!\n")
print('='*50)
print("\nTraining...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=3
)
print("Training completed!")
print('='*50)
print('\nSummary :')
print("\nFinal training accuracy: {:.2f}%".format(history.history['accuracy'][-1] * 100))
print("Final validation accuracy: {:.2f}%".format(history.history['val_accuracy'][-1] * 100))
