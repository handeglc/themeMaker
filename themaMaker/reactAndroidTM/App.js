import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  Image,
} from 'react-native';
import { StackNavigator } from 'react-navigation';

import Main from './src/components/Main';
import LikedCG from "./src/components/LikedCG";


const AppNavigator = StackNavigator({
    Main: { screen: Main },
    LikedCG: { screen: LikedCG}
});

export default class loginAnimation extends Component {
  render() {
    return (
      <AppNavigator />
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5FCFF',
  },
});

AppRegistry.registerComponent('reactAndroidTM', () => reactAndroidTM);