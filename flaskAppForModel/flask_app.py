from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import tensorflow as tf
import io
from waitress import serve

app = Flask(__name__)
CORS(app)

model = tf.keras.models.load_model('model')


def prepare_image(img):
    # Convert the image to a numpy array
    img_array = image.img_to_array(img)

    # Resize the image to match the model's expected input size
    # Change to match the input shape of the model
    img_array = tf.image.resize(img_array, (224, 224))

    img_array = preprocess_input(img_array)

    # The model expects a batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file:
        # Read the image
        image = Image.open(io.BytesIO(file.read())).convert(
            'RGB')  # Ensure image is RGB

        # Prepare the image for the model
        image_array = prepare_image(image)

        # Make a prediction
        predictions = model.predict(image_array)

        confidence_threshold = 0.90  # Adjust the threshold to your needs
        pothole_detected = predictions[0][0] > confidence_threshold
        result = 'Pothole detected' if pothole_detected else 'No pothole detected'
        confidence = float(predictions[0][0])
        return jsonify({'result': result, 'confidence': confidence})

    return jsonify({'error': 'Invalid file'}), 400


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
