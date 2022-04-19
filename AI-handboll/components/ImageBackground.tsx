import React from 'react';
import { ImageBackground, StyleSheet, Text, View } from 'react-native';

const image = { uri: 'C:/utveckling/AI-Handboll/AI-handboll/assets/images/sverige.jpg' };
    
const ImageBackgroundComponent = () => (
    <View style={styles.container}>
        <ImageBackground source={image} resizeMode='cover' style={styles.image}>
        </ImageBackground>
    </View>
);

const styles = StyleSheet.create({
    container: {
        flex: 1
    },
    image: {
        flex: 1,
        justifyContent: 'center',
    },
    text: {
        flex: 1,
        color: 'white',
        fontSize: 42,
        lineHeight: 84,
        fontWeight: 'bold',
        textAlign: 'center',
        backgroundColor: '#000000c0'
    }
});

export default ImageBackgroundComponent;