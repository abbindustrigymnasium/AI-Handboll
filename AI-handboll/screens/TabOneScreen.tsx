import React from 'react';
import { ImageBackground, StyleSheet, Pressable, Alert, Text, View, } from 'react-native';

const image = { uri: 'AI-handboll/assets/images/sverige.jpg' };

const uploadVideoButton = async () => {
  try {
    const response = await fetch('https://54.145.22.116/uploadfile');
    const json = await response.json();
    //spara video?
    console.log(json);
    return json;
  } catch (error) {
    console.error(error);
  }
};

export default function TabOneScreen () {
  return (
      <View style={styles.container}>
        {/* <ImageBackground source={image} resizeMode="cover" style={styles.image}>
        </ImageBackground> */}
      <Pressable
        style={({ pressed }) => [
          {
            backgroundColor: pressed ? 'yellow' : 'blue',
          },
          styles.button,
        ]}
        onPress={() => uploadVideoButton()}>
        <Text style={styles.buttonText}>ladda upp video</Text>
      </Pressable>
      </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'grey',
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    borderRadius: 8,
    padding: 6,
    height: 50,
    width: '70%',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
  },
  buttonText: {
    fontSize: 16,
    color: 'white',
  },
  image: {
    flex: 1,
    justifyContent: 'center',
    width: '100%',
    height: '100%',
  }
});
