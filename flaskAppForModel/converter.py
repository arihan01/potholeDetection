import tensorflow as tf

# Path to the SavedModel directory
saved_model_dir = './model'

# Create a TFLite converter object
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# Convert the model to TFLite format
tflite_model = converter.convert()

# Save the TFLite model to a file
tflite_model_file = 'model_tf.tflite'
with open(tflite_model_file, 'wb') as f:
    f.write(tflite_model)

print('TFLite model conversion completed.')
