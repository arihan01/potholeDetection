# potholeDetection React Native and Flask app 

This repository contains a React Native Android application and a Flask application. The React Native app communicates with the Flask app, which is used for making predictions based on images sent from the device camera. The Flask app sends back a confidence value and a string indicating whether a pothole has been detected.  

## Setting Up and Running the React Native Android App 

- Ensure that you have Node.js installed on your local machine. 

- Run the following commands in the root directory
```npm install``` and ```npm start```

- This will start the development server. You can then open the app on your Android device or emulator. [Reference](https://reactnative.dev/docs/environment-setup) 

- If you want to modify the routes or any other part of the app, you can do so in the `/screens/Detect.js` file.
## Setting Up and Running the Flask App 

- The Flask app is located in a folder called `flaskAppForModel`. Navigate to this folder in your terminal and run flask_app.py.

- This will start the Flask app on `localhost:5000/predict`. 

- If you want to modify the routes or any other part of the app, you can do so in the `flask_app.py` file. 
## How the System Works 

The React Native app captures images from the device camera and sends them to the Flask app. The Flask app uses a machine learning model to make predictions based on these images. The model files are located in a folder within `flaskAppForModel/trained_models`. The Flask app sends back a confidence value and a string. If the confidence value is above 0.90, the string will be "Pothole detected". If the confidence value is below 90, the string will be "No pothole detected". 
## Contributing 

Contributions are welcome. Please feel free to submit a pull request or create an issue.
