import { useColorScheme } from 'react-native';

const Themes = () => {
  const colorScheme = useColorScheme();

  const lightTheme = {
    backgroundColor: '#F5F5F5',
    textColor: '#000000',
    buttonColor: '#FF4081',
  };

  const darkTheme = {
    backgroundColor: '#000',
    textColor: '#F5F5F5',
    buttonColor: '#FF4081',
  };

  return colorScheme === 'dark' ? darkTheme : lightTheme;
};

export default Themes;