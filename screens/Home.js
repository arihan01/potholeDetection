import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  useColorScheme,
  Linking,
} from 'react-native';

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

const getDarkModeColors = isDarkMode => {
  return {
    backgroundColor: isDarkMode ? '#000' : '#F5F5F5',
    textColor: isDarkMode ? '#F5F5F5' : '#000',
    buttonColor: '#FF4081',
  };
};

const Home = ({navigation}) => {
  const isDarkMode = useColorScheme() === 'dark';
  const {backgroundColor, textColor, buttonColor} =
    getDarkModeColors(isDarkMode);

  const openDetectorActivity = () => {
    // const url = 'applinker://detection';
    // Linking.openURL(url).catch(err => console.error('An error occurred', err));
    navigation.navigate('Detect');
  };

  return (
    <View style={[styles.container, {backgroundColor}]}>
      <Text style={[styles.title, {color: textColor}]}>Welcome to My App</Text>
      <Text style={[styles.subtitle, {color: textColor}]}>
        Find and report potholes in your area
      </Text>
      <TouchableOpacity
        style={[styles.button, {backgroundColor: buttonColor}]}
        onPress={openDetectorActivity}>
        <Text style={[styles.buttonText, {color: textColor}]}>
          Detect Potholes
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: screenWidth * 0.06,
    fontWeight: 'bold',
    marginBottom: screenHeight * 0.01,
  },
  subtitle: {
    fontSize: screenWidth * 0.04,
    marginBottom: screenHeight * 0.05,
  },
  button: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: screenHeight * 0.02,
    paddingHorizontal: screenWidth * 0.08,
    borderRadius: 4,
    elevation: 3,
    marginTop: screenHeight * 0.03,
  },
  buttonText: {
    fontSize: screenWidth * 0.04,
    lineHeight: 21,
    fontWeight: 'bold',
    letterSpacing: 0.25,
  },
});

export default Home;
