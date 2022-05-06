import React from 'react';
import { StyleSheet, Pressable, Text, View } from 'react-native';
import DocumentPicker from "react-native-document-picker";

let bodyContent = new FormData();
bodyContent.append('data', 'C:/utveckling/AI-Handboll/AI-handboll/Test.txt');

let pickFile = async() => {
  //pick a single file
  console.log(DocumentPicker.pick())
  try {
    const res = await DocumentPicker.pick({
      type: [DocumentPicker.types.video, DocumentPicker.types.plainText],//flera types ex: [DocumentPicker.types.csv, DocumentPicker.types.txt]
    });
    console.log(res);
  } catch (err) {
    if (DocumentPicker.isCancel(err)) {
      console.log("error -----", err);
    } else {
      throw err;
    }
  }
}

const uploadVideoButton = async () => {
  try {
    pickFile()
    const response = await fetch('https://54.145.22.116/uploadfile', {
      method: "POST",
      body: bodyContent,
      mode: 'no-cors'
      // headers: headersList
    }).then(function (response) {
      return response.text();
    }).then(function (data) {
      console.log(data); })    
}
  catch(e){
    console.log(e);
  };
};

export default function TabOneScreen () {
  return (
      <View style={styles.container}>
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
  },})
