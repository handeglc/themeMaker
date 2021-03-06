import React, {Component} from 'react';
import {
  View,
  Text,
  Button,
  ScrollView,
} from 'react-native';

// const DEVICE_WIDTH = Dimensions.get('window').width;
// const DEVICE_HEIGHT = Dimensions.get('window').height;

export default class LikedCG extends Component {

  constructor(props) {
    super(props);
    this.state = {
        response: 'no message',
        token: this.props.navigation.getParam('token'),
        logged: this.props.navigation.getParam('logged'),
    };
    this.recommend = this.recommend.bind(this);
    LikedCG.delete_cg = LikedCG.delete_cg.bind(this);

  }


  recommend(){
      console.log("recommend button");
      fetch("http://10.2.2.107:8000/api/login/", {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: "Token " + this.state.token,
      },
      body: JSON.stringify({
        operation: 'recommend',
      }),

      }).then(function(response) {
          return response.json();
      }).then(data => {
          console.log("hey00000000");
          console.log(data);
          this.props.navigation.navigate('PresentedColors', {colors: data["color_list"], token: this.state.token, uri: "none"});
      }).catch(function(ex) {
          console.log("parsing failed", ex);
      });
  }

  static delete_cg(cg_id){
      console.log("delete button "+ cg_id);
      fetch("http://10.2.2.107:8000/api/login/", {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: "Token " + this.state.token,
      },
      body: JSON.stringify({
        operation: 'delete_cg',
        cg_id: cg_id,
      }),

      }).then(function(response) {
          return response.json();
      }).then(data => {
          console.log(data);
          if(data["deleted"] === "true"){
              this.props.navigation.navigate('LikedCG', {liked_cg: data["liked_cg"], token: this.state.token});
          }

      }).catch(function(ex) {
          console.log("parsing failed", ex);
      });
  }


    render() {
        const { navigation } = this.props;
        const liked_cg = navigation.getParam('liked_cg');
        console.log("liked'a geldik");
        console.log(this.state.token);

        const cgs = [];

        for(let i = 0; i < liked_cg.length; i++){
            const cg_colors = [];
            for(let j = 0; j < liked_cg[i]["list"].length; j++){
                cg_colors.push(
                    <View  key={"color"+j} style = {{ backgroundColor: liked_cg[i]["list"][j], width:100, heigth:100, flexDirection: 'row'}}>
                        <Text> {liked_cg[i]["list"][j]} </Text>
                    </View>
                )
            }
            cgs.push(
                <View key = {i} style = {{ flexDirection: 'column', marginBottom:30, alignItems: 'center',}}>
                    {cg_colors}
                    <View style={{marginTop:5, fontSize:5,}}>
                        <Button
                              onPress={() => LikedCG.delete_cg(liked_cg[i]["id"])}
                              title="Delete"
                              color="#5FF07F"

                              //cg_id = cg[j]
                            />
                    </View>
                </View>
            )
        }

        return (


            <View style={{flexDirection: 'column', }}>
                <ScrollView>
                <Text>Your liked Color Groups</Text>
                    { cgs }
                    <Button
                      onPress={this.recommend}
                      title="Recommend"
                      color="#64857F"
                    />
                    <Button
                      onPress={() => this.props.navigation.navigate('Cam',{token: this.state.token})}
                      title="Open Camera"
                    />
                 </ScrollView>
            </View>



        );
  }

}

