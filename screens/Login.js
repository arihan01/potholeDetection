/**
 * This file contains the implementation of the Login.
 * The screen allows users to log in with their username and password, or register a new account.
 * It uses the @react-native-firebase/auth library for authentication.
 * Remember to change the google-services.json file in the android/app folder to your own Firebase project.
 */

import React, {useState} from 'react';
import {
  View,
  Text,
  TextInput,
  Button,
  StyleSheet,
  ToastAndroid,
  Dimensions,
  useColorScheme,
} from 'react-native';
import auth from '@react-native-firebase/auth';

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

const getDarkModeColors = isDarkMode => {
  return {
    backgroundColor: isDarkMode ? '#000' : '#F5F5F5',
    textColor: isDarkMode ? '#F5F5F5' : '#333',
    borderColor: '#333',
    buttonColor: '#333',
  };
};

const Login = ({navigation}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const scheme = useColorScheme();
  const isDark = scheme === 'dark';
  const {backgroundColor, textColor, borderColor, buttonColor} =
    getDarkModeColors(isDark);
  const showToast = message => {
    ToastAndroid.show(message, ToastAndroid.SHORT);
  };

  return (
    <View style={[styles.container, {backgroundColor}]}>
      <Text style={[styles.heading, {color: textColor}]}>Log In</Text>
      <Text style={[styles.subheading, {color: textColor}]}>
        Please enter your username and password
      </Text>
      <TextInput
        style={[
          styles.input,
          {
            color: textColor,
            borderColor: borderColor,
          },
        ]}
        placeholder="Email"
        placeholderTextColor="#A9A9A9"
        value={username}
        onChangeText={text => setUsername(text)}
        accessibilityLabel="Email"
      />
      <TextInput
        style={[
          styles.input,
          {
            color: textColor,
            borderColor: borderColor,
          },
        ]}
        placeholder="Password"
        placeholderTextColor="#A9A9A9"
        value={password}
        onChangeText={text => setPassword(text)}
        secureTextEntry
        accessibilityLabel="Password"
      />
      <Button
        style={[
          styles.button,
          {
            backgroundColor: buttonColor,
            color: textColor,
          },
        ]}
        title="Log In"
        onPress={() => {
          if (username === '' || password === '') {
            showToast('Please fill in all fields');
          } else {
            auth()
              .signInWithEmailAndPassword(username, password)
              .then(() => {
                console.log('User account signed in!');
                navigation.navigate('Home');
              })
              .catch(error => {
                console.error(error);
                showToast('Wrong username or password');
              });
          }
        }}
        color="#333"
        accessibilityLabel="Log In"
      />
      <Text style={[styles.accountText, {color: textColor}]}>
        Don't have an account? Enter credentials and click Register
      </Text>
      <Text
        style={[styles.registerText, {color: '#FF4081'}]}
        onPress={() => {
          if (username === '' || password === '') {
            showToast('Please fill in all fields');
          } else {
            auth()
              .createUserWithEmailAndPassword(username, password)
              .then(() => {
                console.log('User account created & signed in!');
                navigation.navigate('Home');
              })
              .catch(error => {
                if (error.code === 'auth/email-already-in-use') {
                  console.log('That email address is already in use!');
                  showToast('An account with this email already exists');
                }

                if (error.code === 'auth/invalid-email') {
                  console.log('That email address is invalid!');
                  showToast('Please enter a valid email address');
                }

                console.error(error);
              });
          }
        }}>
        Register
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: screenWidth * 0.05,
  },
  heading: {
    fontSize: screenWidth * 0.1,
    fontWeight: 'bold',
    marginBottom: screenWidth * 0.02,
  },
  subheading: {
    fontSize: screenWidth * 0.03,
    marginBottom: screenWidth * 0.04,
  },
  input: {
    height: screenHeight * 0.06,
    borderWidth: 1,
    marginBottom: screenHeight * 0.02,
    padding: screenWidth * 0.02,
    borderRadius: 5,
  },
  registerText: {
    fontSize: screenWidth * 0.04,
    marginTop: screenHeight * 0.02,
    textAlign: 'center',
  },
  button: {
    height: screenHeight * 0.1,
    lineHeight: screenHeight * 0.09,
    marginTop: screenHeight * 0.02,
    textAlign: 'center',
    borderRadius: 6,
  },
  accountText: {
    fontSize: screenWidth * 0.03,
    textAlign: 'center',
    marginTop: screenHeight * 0.03,
  },
});

export default Login;