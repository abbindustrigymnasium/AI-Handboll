// import React, { Component, useState, useEffect } from 'react';
// import { StyleSheet, Pressable, Text, View, Button, Image, Platform } from 'react-native';
// import DocumentPicker from "react-native-document-picker";
// import * as ImagePicker from 'react-native-image-picker';
// import { Button, Image, Platform } from 'react-native';

// import React from 'react';

// const [response, setResponse] = React.useState<any>(null);

// ImagePicker.launchImageLibrary({
//   selectionLimit: 0,
//   mediaType: 'photo',
//   includeBase64: false,
// }, setResponse)

import * as React from 'react';
import { Text, View, StyleSheet, Image, Platform } from 'react-native';
import { FAB, Portal, Provider } from 'react-native-paper';
import { launchCamera, launchImageLibrary } from 'react-native-image-picker';

export default function TabOneScreen () {
  const [state, setState] = React.useState({ open: false });

  const onStateChange = ({ open }) => setState({ open });

  const [response, setResponse] = React.useState<any>(null);

  const { open } = state;
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      {response?.assets &&
        response?.assets.map(({ uri }) => (
          <View key={uri} style={styles.image}>
            <Image
              resizeMode="cover"
              resizeMethod="scale"
              style={{ width: 200, height: 200 }}
              source={{ uri: uri }}
            />
          </View>
        ))}
      <Provider>
        <Portal>
          <FAB.Group
            fabStyle={styles.fab}
            open={open}
            icon={open ? 'minus' : 'plus'}
            actions={[
              {
                icon: 'camera', small: false, onPress: () => {
                  launchCamera({
                    saveToPhotos: true,
                    mediaType: 'photo',
                    includeBase64: false,
                  }, setResponse)
                }
              },
              {
                icon: 'image-area',
                small: false,
                onPress: () => {
                  launchImageLibrary({
                    selectionLimit: 0,
                    mediaType: 'photo',
                    includeBase64: false,
                  }, setResponse)
                },
              },
            ]}
            onStateChange={onStateChange}
            onPress={() => {
              if (open) {
                // do something if the speed dial is open
              }
            }}
          />
        </Portal>
      </Provider>
    </View>
  );
}

const styles = StyleSheet.create({
  fab: {
    backgroundColor: '#EA5B70',
  },
  image: {
    marginVertical: 24,
    alignItems: 'center',
  }
})

// let bodyContent = new FormData();
// bodyContent.append('data', 'C:/utveckling/AI-Handboll/AI-handboll/Test.txt');

// export function videoPicker () {
//   const [image, setImage] = useState(null);

//   const pickImage = async () => {
//     // No permissions request is necessary for launching the image library
//     let result = await ImagePicker.launchImageLibraryAsync({
//       mediaTypes: ImagePicker.MediaTypeOptions.All,
//       allowsEditing: true,
//       aspect: [4, 3],
//       quality: 1,
//     });

//     console.log(result);

//     if (!result.cancelled) {
//       setImage(result.uri);
//     }
//   };

//   return (
//     <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
//       <Button title="Pick an image from camera roll" onPress={pickImage} />
//       {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
//     </View>
//   );
// }

// // let selectVideo = async () => {
// //   ImagePicker.launchImageLibrary({ mediaType:'video', includeBase64: true }, (response) => {
// //     this.setState({ video: response });
// //   })
// // }

// let pickFile = async() => {
//   //pick a single file
//   console.log(DocumentPicker.pick())
//   try {
//     const res = await DocumentPicker.pick({
//       type: [DocumentPicker.types.video, DocumentPicker.types.plainText],//flera types ex: [DocumentPicker.types.csv, DocumentPicker.types.txt]
//     });
//     console.log(res);
//   } catch (err) {
//     if (DocumentPicker.isCancel(err)) {
//       console.log("error -----", err);
//     } else {
//       throw err;
//     }
//   }
// }

// const uploadVideoButton = async () => {
//   try {
//     // pickFile()
//     const response = await fetch('https://54.145.22.116/uploadfile', {
//       method: "POST",
//       body: bodyContent,
//       mode: 'no-cors'
//       // headers: headersList
//     }).then(function (response) {
//       return response.text();
//     }).then(function (data) {
//       console.log(data); })    
// }
//   catch(e){
//     console.log(e);
//   };
// };

// export default function TabOneScreen () {
//   return (
//       <View style={styles.container}>
//       <Pressable
//         style={({ pressed }) => [
//           {
//             backgroundColor: pressed ? 'yellow' : 'blue',
//           },
//           styles.button,
//         ]}
//         onPress={() => uploadVideoButton()}>
//         <Text style={styles.buttonText}>ladda upp video</Text>
//       </Pressable>
//       </View>
//   );
// };

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     backgroundColor: 'grey',
//     justifyContent: 'center',
//     alignItems: 'center',
//   },
//   button: {
//     borderRadius: 8,
//     padding: 6,
//     height: 50,
//     width: '70%',
//     justifyContent: 'center',
//     alignItems: 'center',
//     elevation: 5,
//   },
//   buttonText: {
//     fontSize: 16,
//     color: 'white',
//   },
//   image: {
//     flex: 1,
//     justifyContent: 'center',
//     width: '100%',
//     height: '100%',
//   },})
