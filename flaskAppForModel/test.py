import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from keras.models import load_model

# Constants
IMAGE_SIZE = (300, 300)
MODEL_PATH = 'full_model.h5'

# Function to load the model


def load_model_from_file(model_path):
    return load_model(model_path)

# Function to preprocess the image


def preprocess_image(image, target_size):
    if image.shape[-1] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_resized = cv2.resize(image, target_size)
    image_normalized = image_resized.astype('float32') / 255.0
    image_normalized = image_normalized.reshape(1, *target_size, 1)
    return image_normalized


class PotholePredictionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.model = load_model_from_file(MODEL_PATH)

        # Initialize video capture
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        # Retrieve the width and height of the video source
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        # Button to select an image and predict
        self.btn_predict = tk.Button(
            window, text="Predict on Image", width=50, command=self.predict_on_image)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        # Button to start real-time prediction
        self.btn_realtime = tk.Button(
            window, text="Start Real-time Prediction", width=50, command=self.toggle_realtime_prediction)
        self.btn_realtime.pack(anchor=tk.CENTER, expand=True)

        self.is_realtime = False
        self.delay = 15
        self.update()

        self.window.mainloop()

    def predict_on_image(self):
        path = filedialog.askopenfilename()
        if path:
            image = cv2.imread(path, cv2.IMREAD_COLOR)
            processed_image = preprocess_image(image, IMAGE_SIZE)
            prediction = self.model.predict(processed_image)
            self.show_prediction(prediction, image)

    def show_prediction(self, prediction, image):
        # Create a new window to display the prediction and image
        result_window = tk.Toplevel(self.window)
        result_window.title("Prediction Result")

        # Convert the image to a format that can be displayed in Tkinter
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        # Resize to fit the window
        image.thumbnail((500, 500), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Display the image in a label
        label_image = tk.Label(result_window, image=photo)
        label_image.image = photo  # Keep a reference!
        label_image.pack(side="top", fill="both", expand="yes")

        # Determine the prediction result
        # Assuming binary classification [pothole, no pothole]
        pothole_probability = prediction[0][0]
        pred_text = f"Pothole Probability: {pothole_probability: .2%}"

        # Display the prediction result in a label
        label_prediction = tk.Label(result_window, text=pred_text)
        label_prediction.pack(side="top", fill="both", expand="yes")

    def toggle_realtime_prediction(self):
        self.is_realtime = not self.is_realtime
        if self.is_realtime:
            self.btn_realtime.configure(text="Stop Real-time Prediction")
        else:
            self.btn_realtime.configure(text="Start Real-time Prediction")

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()
        if ret:
            # Resize the frame to fit the canvas
            frame = cv2.resize(frame, (int(self.width), int(self.height)))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            # Update the canvas image to the center
            self.canvas.create_image(
                self.width // 2, self.height // 2, image=self.photo, anchor=tk.CENTER)

            if self.is_realtime:
                self.realtime_predict(frame)

        self.window.after(self.delay, self.update)

    def realtime_predict(self, frame):
        processed_frame = preprocess_image(frame, IMAGE_SIZE)
        prediction = self.model.predict(processed_frame)
        # Update the frame with the prediction result if necessary
        # Assuming binary classification [pothole, no pothole]
        pothole_probability = prediction[0][0]
        pred_text = f"Pothole: {pothole_probability: .2%}"
        cv2.putText(frame, pred_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


if __name__ == "__main__":
    root = tk.Tk()
    PotholePredictionApp(root, "Pothole Prediction App")
