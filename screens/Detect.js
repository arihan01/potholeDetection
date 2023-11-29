import React, {useState, useEffect} from 'react';
import {View, Text, StyleSheet, Dimensions, useColorScheme} from 'react-native';
import {RNCamera} from 'react-native-camera';
import axios from 'axios';

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

const getDarkModeColors = isDarkMode => {
  return {
    backgroundColor: isDarkMode ? '#000' : '#F5F5F5', // Set background color based on dark mode
    textColor: isDarkMode ? '#F5F5F5' : '#000', // Set text color based on dark mode
  };
};

const Detect = () => {
  const scheme = useColorScheme();
  const isDark = scheme === 'dark';
  const {backgroundColor, textColor} = getDarkModeColors(isDark);
  const [data, setData] = useState(''); // State to store data
  const [isCapturing, setIsCapturing] = useState(false); // State to track if capturing is in progress
  const [isCameraReady, setIsCameraReady] = useState(false); // State to track if camera is ready
  const [confidence, setConfidence] = useState(0); // State to store confidence level

  const takePicture = async camera => {
    if (isCapturing) {
      return;
    }
    setIsCapturing(true);
    const options = {quality: 0.5, base64: true};
    const imageData = await camera.takePictureAsync(options); // Take picture using camera
    // construct form data
    const formData = new FormData();
    formData.append('file', {
      uri: imageData.uri,
      type: 'image/jpeg',
      name: 'image.jpg',
    });

    try {
      const response = await axios.post(
        'localhost:5000/predict', // Send image data to prediction endpoint (found inside ./flaskAppForModel/flask_app.py)
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      );
      setData(response.data.result); // Update data state with response data
      setConfidence(response.data.confidence); // Update confidence state with response confidence
    } catch (error) {
      console.error('Error sending data: ', error);
    } finally {
      setIsCapturing(false);
    }
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (this.camera && !isCapturing && isCameraReady) {
        takePicture(this.camera); // Take picture at regular intervals if camera is ready and not capturing
      }
    }, 500); // Take picture every 0.5 second

    return () => clearInterval(intervalId);
  }, [isCapturing, isCameraReady]); // Only re-run the effect if isCapturing changes

  return (
    <View style={[styles.container, {backgroundColor}]}>
      <RNCamera
        ref={ref => {
          this.camera = ref;
        }}
        style={styles.preview}
        type={RNCamera.Constants.Type.back}
        captureAudio={false}
        onCameraReady={() => setIsCameraReady(true)} // Set isCameraReady state to true when camera is ready
      />
      <View style={{flex: 0, flexDirection: 'row', justifyContent: 'center'}}>
        <Text
          style={{
            color: textColor,
            marginBottom: 40,
            fontSize: 24,
            fontWeight: 'bold',
          }}>
          {confidence > 0.9 ? `(${(confidence * 100).toFixed(2)}%)` : `(${(confidence * 100).toFixed(2)}%)`} // Display confidence percentage
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'black',
  },
  preview: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
});

export default Detect;