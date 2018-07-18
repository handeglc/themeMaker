import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Dimensions from 'Dimensions';
import {
  StyleSheet,
  KeyboardAvoidingView,
  View,
  ActivityIndicator,
  TouchableOpacity,
  Image,
  Text,
  Button,
} from 'react-native';

import UserInput from './UserInput';



export default class Main extends Component {

  constructor(props) {
    super(props);
    this.state = {
      showPass: true,
      press: false,
      username: 'username',
      //pass: 'pass',
    };
    this.showPass = this.showPass.bind(this);
    this.onPressFunc = this.onPressFunc.bind(this);

  }


  showPass() {
    this.state.press === false
      ? this.setState({showPass: false, press: true})
      : this.setState({showPass: true, press: false});
  }

  onPressFunc() {
    console.log('clicked button');
    fetch("http://localhost:8000/show_cg", {
      method: "GET",

  }).then(function(response) {
      return response.json();
  }).then(function(data) {
      console.log("Data is ok", data);
  }).catch(function(ex) {
      console.log("parsing failed", ex);
  });
  }

  render() {
    console.log("heeey i am here");
    return (
      <KeyboardAvoidingView behavior="padding" style={styles.container}>
          <Text>Login Page</Text>
        <UserInput
          value={this.state.textValue}
          placeholder="Username"
          autoCapitalize={'none'}
          returnKeyType={'done'}
          autoCorrect={false}
        />
        <UserInput

          secureTextEntry={this.state.showPass}
          placeholder="Password"
          returnKeyType={'done'}
          autoCapitalize={'none'}
          autoCorrect={false}
        />
        <TouchableOpacity
          activeOpacity={0.7}
          style={styles.btnEye}
          onPress={this.showPass}>

        </TouchableOpacity>
        <Button
          style={styles.btnEye}
          onPress={this.onPressFunc}
          title="Login"
          color="#64857F"
          accessibilityLabel="Learn more about this purple button"
        />
      </KeyboardAvoidingView>
    );
  }
}

const DEVICE_WIDTH = Dimensions.get('window').width;
const DEVICE_HEIGHT = Dimensions.get('window').height;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },
  btnEye: {
    position: 'absolute',
    right: 28,
    bottom:50,

  },
  iconEye: {
    width: 25,
    height: 25,
    tintColor: 'rgba(0,0,0,0.2)',
  },
});