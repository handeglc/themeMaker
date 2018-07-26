import React, {Component} from 'react';
import {
  View,
  Text,
  ScrollView,
  Image,
  Dimensions,
  TextInput,
  Button,
  Alert,
} from 'react-native';
import LikedCG from "./LikedCG";

 const DEVICE_WIDTH = Dimensions.get('window').width;
 // const DEVICE_HEIGHT = Dimensions.get('window').height;

export default class PresentedColors extends Component {

  constructor(props) {
    super(props);
    this.state = {
        color: "#ffffff",
        token: this.props.navigation.getParam('token'),
    };
        this.add_cg = this.add_cg.bind(this);
  }


  add_cg(colors){
      console.log("add_cg start");
      console.log(colors);
      console.log(this.state.token);
      if(this.state.token === "0"){
        Alert.alert(
          'Not Authorized',
          'You should log in first!',
          [
            {text: 'OK'},
            {text: 'Login', onPress: () => this.props.navigation.navigate('Main')},
          ],
          { cancelable: false }
        )
      }else{
          fetch("http://10.2.2.107:8000/api/login/", {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: "Token " + this.state.token,
          },
          body: JSON.stringify({
            operation: 'add_cg',
            colors: colors,
          }),

          }).then(function(response) {
              return response.json();
          }).then(data => {
              console.log("add_cg fetch ----");
              console.log(data);
              this.props.navigation.navigate('LikedCG', {liked_cg: data["liked_cg"], token: this.state.token});

          }).catch(function(ex) {
              console.log("parsing failed", ex);
          });
      }

  }


    render() {
        const { navigation } = this.props;
        const cg = navigation.getParam('colors');
        console.log("presentedcolors geldik");

        const uri = navigation.getParam('uri');
        const image = uri !== "none";
        console.log(image);

        const cg_colors = [];
        for(let j = 0; j < cg.length; j++){
            cg_colors.push(
                <View  key={"color"+j}
                       style = {{ backgroundColor: cg[j], height:30,}}
                       onPress={() => this.setState({color: cg[j]})}
                >
                    <Text> {cg[j]} </Text>
                </View>
            )
        }


        if (image){
            console.log("pushing image");
            cg_colors.push(
                <View  key={uri}>
                   <Text style={{ textAlign: 'center', fontSize:17,}}>Choose the color from above</Text>
                    <View key={"button"} style={{marginTop:15, fontSize:5, width: 50, alignItems: 'center'}}>
                        <Button
                          onPress={() => this.add_cg(cg)}
                          title="Like"
                          color="#5F1070"

                          //cg_id = cg[j]
                        />
                    </View>
                   <Image
                    style={{width: DEVICE_WIDTH, height: 500, marginTop:10,}}
                    source={{uri: uri}}
                    />
                </View>
            );
        }else{
            cg_colors.push(
                <View key={"button"} style={{marginTop:15, fontSize:5, width: 50, alignItems: 'center'}}>
                    <Button
                      onPress={() => this.add_cg(cg)}
                      title="Like"
                      color="#5F107F"

                      //cg_id = cg[j]
                    />
                </View>
            );
        }


        return (


            <View style={{flexDirection: 'column', }}>
                <ScrollView>

                    { cg_colors }
                    <TextInput

                        style={{width: DEVICE_WIDTH - 40,
                                height: 40,
                                color: this.state.color}}
                    />
                 </ScrollView>
            </View>



        );
  }

}

