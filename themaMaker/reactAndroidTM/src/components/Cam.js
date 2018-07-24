import React, { Component } from 'react';
import {
  AppRegistry,
  Dimensions,
  StyleSheet,
  Text,
  TouchableOpacity,
  View
} from 'react-native';
import { RNCamera } from 'react-native-camera';

export default class Cam extends Component {
  constructor(props) {
    super(props);
    this.state = {
        token: this.props.navigation.getParam('token'),
    };

  }

  render() {
    return (
      <View style={styles.container}>
        <RNCamera
            ref={ref => {
              this.camera = ref;
            }}
            style = {styles.preview}
            type={RNCamera.Constants.Type.back}
            flashMode={RNCamera.Constants.FlashMode.on}
            permissionDialogTitle={'Permission to use camera'}
            permissionDialogMessage={'We need your permission to use your camera phone'}
        />
        <View style={{flex: 0, flexDirection: 'row', justifyContent: 'center',}}>
        <TouchableOpacity
            onPress={this.takePicture.bind(this)}
            style = {styles.capture}
        >
            <Text style={{fontSize: 14}}> SNAP </Text>
        </TouchableOpacity>
        </View>
      </View>
    );
  }

  takePicture = async function() {
    if (this.camera) {
        const options = { quality: 0.5, base64: true };
        const data = await this.camera.takePictureAsync(options)
        console.log(data.uri);
        //this.props.navigation.navigate('LikedCG');
        const data_p = new FormData();
        data_p.append('name', 'testName'); // you can append anyone.
        data_p.append('operation', 'dominantColors')
        data_p.append('photo', {
          uri: data.uri,
          type: 'image/jpeg', // or photo.type
          name: 'photoToAnalyze.jpg'
        });
        fetch("http://10.2.2.107:8000/api/login/", {
          method: 'post',
          headers: {
            Authorization: "Token " + this.state.token,
          },
          body: data_p
        }).then(res => {
          console.log(res);
        });
    }
  };
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'black'
  },
  preview: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center'
  },
  capture: {
    flex: 0,
    backgroundColor: '#fff',
    borderRadius: 5,
    padding: 15,
    paddingHorizontal: 20,
    alignSelf: 'center',
    margin: 20
  }
});