import os
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt


def create_pretrained_model(input_shape, num_classes=1):
    base_model = MobileNetV2(
        weights='imagenet', include_top=False, input_shape=input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='sigmoid',
                        kernel_regularizer=regularizers.l2(0.01))(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    for layer in base_model.layers:
        layer.trainable = False
    return model


def setup_data_augmentation():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    validation_datagen = ImageDataGenerator(rescale=1./255)

    return train_datagen, validation_datagen


def setup_callbacks():
    checkpoint = ModelCheckpoint(
        'model  ', monitor='val_loss', save_best_only=True, verbose=1)
    early_stop = EarlyStopping(monitor='val_loss', patience=10, verbose=1)
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss', factor=0.2, patience=5, min_lr=0.001, verbose=1)
    return [checkpoint, early_stop, reduce_lr]


def train_model(model, train_generator, validation_generator, callbacks):
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        epochs=50,
        validation_data=validation_generator,
        validation_steps=max(1, validation_generator.samples //
                             validation_generator.batch_size),
        callbacks=callbacks
    )
    return history


def plot_history(history):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    if 'val_accuracy' in history.history:
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.title('Accuracy over epochs')

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    if 'val_loss' in history.history:
        plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.title('Loss over epochs')
    plt.show()


# Assuming the script is to be run directly, the following lines would execute the training.
if __name__ == '__main__':
    input_shape = (224, 224, 3)
    num_classes = 1  # Assuming binary classification (pothole or not)
    model = create_pretrained_model(input_shape, num_classes)
    train_datagen, validation_datagen = setup_data_augmentation()

    # Setup data generators (assuming the presence of 'train' and 'validation' directories)
    train_generator = train_datagen.flow_from_directory(
        './My Dataset/train',
        target_size=(input_shape[0], input_shape[1]),
        batch_size=32,
        class_mode='binary'
    )

    validation_generator = validation_datagen.flow_from_directory(
        './My Dataset/test',
        target_size=(input_shape[0], input_shape[1]),
        batch_size=32,
        class_mode='binary'
    )

    callbacks = setup_callbacks()
    model.compile(optimizer=Adam(lr=0.0001),
                  loss='binary_crossentropy', metrics=['accuracy'])
    history = train_model(model, train_generator,
                          validation_generator, callbacks)
    plot_history(history)
