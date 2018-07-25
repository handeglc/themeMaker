import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
} from 'react-native';
import { StackNavigator } from 'react-navigation';

import Main from './src/components/Main';
import LikedCG from "./src/components/LikedCG";
import Cam from "./src/components/Cam";
import PresentedColors from "./src/components/PresentedColors";


const AppNavigator = StackNavigator({
    Main: { screen: Main },
    LikedCG: { screen: LikedCG},
    Cam: { screen: Cam },
    PresentedColors: { screen: PresentedColors}
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