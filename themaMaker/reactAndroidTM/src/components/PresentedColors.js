import React, {Component} from 'react';
import {
  View,
  Text,
  ScrollView,
  Image,
  Dimensions,
  TextInput,
} from 'react-native';

 const DEVICE_WIDTH = Dimensions.get('window').width;
 // const DEVICE_HEIGHT = Dimensions.get('window').height;

export default class PresentedColors extends Component {

  constructor(props) {
    super(props);
    this.state = {
        color: "#ffffff",
        token: this.props.navigation.getParam('token'),
    };

  }




    render() {
        const { navigation } = this.props;
        const cg = navigation.getParam('colors');
        console.log("liked'a geldik");
        console.log(this.state.token);

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
                   <Image
                    style={{width: DEVICE_WIDTH, height: 500, marginTop:10,}}
                    source={{uri: uri}}
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

