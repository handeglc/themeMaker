import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  KeyboardAvoidingView,
  View,
  ActivityIndicator,
  TouchableOpacity,
  Image,
  Text,
  Button,
  TextInput,
  Dimensions,
} from 'react-native';

import UserInput from './LikedCG';



export default class Main extends Component {

  constructor(props) {
    super(props);
    this.state = {
      showPass: true,
      press: false,
      username: 'username',
      pass: 'pass',
      response: 'no message',
    };
    this.showPass = this.showPass.bind(this);
    this.onPressFunc = this.onPressFunc.bind(this);
    //this.onChange = this.onChange.bind(this);

  }


  showPass() {
    this.state.press === false
      ? this.setState({showPass: false, press: true})
      : this.setState({showPass: true, press: false});
  }

  onPressFunc() {
    console.log('clicked button');
    console.log(this.state.username);
    console.log(this.state.pass);
    fetch("http://10.2.2.107:8000/api/login/", {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        operation: 'login',
        username: this.state.username,
        password: this.state.pass,
      }),

  }).then(function(response) {

      //console.log(response);
      return response.json();
  }).then(data => {
      //console.log("data is:")
      console.log(data["token"]);
      //console.log( JSON.stringify(data["liked_cg"]) );
      if (data["message"] !== "done"){

        this.setState({ response: data["message"] });
        //console.log(this.state.response);
      }else{
          this.props.navigation.navigate('LikedCG', {liked_cg: data["liked_cg"], token: data["token"],});
      }
      //console.log("Data is ok", data);
  }).catch(function(ex) {
      console.log("parsing failed", ex);
  });
  }

    render() {
    console.log("heeey i am here");
    return (
      <KeyboardAvoidingView behavior="padding" style={styles.container}>
        <Text>Login Page</Text>
        <Text>{this.state.response}</Text>
        <View style={styles.inputWrapper}>

          <TextInput
            style={styles.input}
            placeholder={this.props.placeholder}
            secureTextEntry={this.props.secureTextEntry}
            autoCorrect={this.props.autoCorrect}
            autoCapitalize={this.props.autoCapitalize}
            returnKeyType={this.props.returnKeyType}
            placeholderTextColor="white"
            underlineColorAndroid="transparent"
            onChangeText={(username) => this.setState({username})}
            placeholder="Username"
            autoCapitalize={'none'}
            returnKeyType={'done'}
            autoCorrect={false}
          />
          <TextInput
            style={styles.input}
            placeholder={this.props.placeholder}
            secureTextEntry={this.props.secureTextEntry}
            autoCorrect={this.props.autoCorrect}
            autoCapitalize={this.props.autoCapitalize}
            returnKeyType={this.props.returnKeyType}
            placeholderTextColor="white"
            underlineColorAndroid="transparent"
            onChangeText={(pass) => this.setState({pass})}
            secureTextEntry={this.state.showPass}
            placeholder="Password"
            returnKeyType={'done'}
            autoCapitalize={'none'}
            autoCorrect={false}
          />
        <Button
          style={styles.btnEye}
          onPress={this.onPressFunc}
          title="Login"
          color="#64857F"
          accessibilityLabel="Learn more about this purple button"
        />
      </View>

        <TouchableOpacity
          activeOpacity={0.7}
          style={styles.btnEye}
          onPress={this.showPass}>
        </TouchableOpacity>

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
  input: {
    backgroundColor: '#89b9b3',
    width: DEVICE_WIDTH - 40,
    height: 40,
    marginHorizontal: 20,
    paddingLeft: 45,
    borderRadius: 20,
    color: '#04090a',
    marginBottom: 20,
  },
  inputWrapper: {
    flex: 1,
  },
});