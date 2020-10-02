import React from 'react';
import { StyleSheet, Text, View, Image, Button, ScrollView} from 'react-native';
import { AppLoading } from 'expo';
import * as Font from 'expo-font';

import SongList from "../components/songList";

let customFonts  = {
  'FuturaH': require('../assets/fonts/futurah.ttf'),
  'FuturaL': require('../assets/fonts/futural.ttf'),
};

export default class Find extends React.Component  {
  state = {
    fontsLoaded: false,
    playing: false,
  };

  async _loadFontsAsync() {
    await Font.loadAsync(customFonts);
    this.setState({ fontsLoaded: true });
  }

  componentDidMount() {
    this._loadFontsAsync();
    this.getLoc()
    this.getloc=setInterval(() => {
  this.getLoc()
}, 60000);

  }

  getLoc(){
    fetch('https://us-central1-aiot-fit-xlab.cloudfunctions.net/autoplaygeneral', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({"action": "location", "lat" : 2.2222, "lon": 45.225, "email":"e@mail.com"})
})
    .then((response) => response.json())
    .then((responseJson) => {
console.log(responseJson);
    })
    .catch((error) => {
        console.error(error);
    });
  }

  
  getData() {
    return  [
    {
      
    name:"Nand's Parking",
    artist:"Drenchill, Indiiana",
  },
  {
    
    name:"Dance with Me (feat. Thomas Rhett & Young Thug)",
    artist:"Diplo, Thomas Rhett, Young Thug",
  },
  {
    
    name:"Upside Down",
    artist:"Nayio Bitz, Nikko Culture",
  },
  {
    
    name:"This Is Real (ft. Ella Henderson)",
    artist:"Jax Jones, Ella Henderson",
  },
  ]
  }

  render(){
    if (this.state.fontsLoaded) {
    return (
    <View style={styles.container}>
      
     
    

     
            <Text style={{position:'relative',fontSize:50,marginTop:'20%',textAlign:'center', color:'#364f6b', fontFamily:'FuturaH'}}>Explore</Text>
           

            
     

      <Text style={{position:'relative',fontSize:20,marginTop:'10%',marginLeft:'5%', textAlign:'left', color:'#364f6b', fontFamily:'FuturaH'}}>Parking spots nearby</Text>
    
      <ScrollView style={styles.scrollcontainer}>
      <SongList itemList={this.getData()}/>
      </ScrollView>
      
      
    </View>
    );
    }
    else {
    return <AppLoading />;
    }
  }
}

const styles = StyleSheet.create({
  container: {
    height:'100%',
    position:'relative',
    backgroundColor:'#f5f5f5'
  },
  left:{
    height:'7%',
    width:'7%',
    top:'2.5%',
    resizeMode:'contain',
    left:'5%',
    position:'absolute',
  },
  right:{
    height:'7%',
    width:'7%',
    top:'2.5%',
    resizeMode:'contain',
    right:'5%',
    position:'absolute'
  },
  middle:{
    height:'60%',
    width:'60%',
    marginTop:'5%',
    resizeMode:'contain',
    zIndex:3,
    alignSelf:'center',
  },
  album:{
    height:'40%',
    width:'50%',
    marginTop:'7.5%',
    resizeMode:'contain',
    zIndex:3,
    alignSelf:'center',
    borderRadius:10,
  },
  spotify:{
    height:'100%',
    width:'8%',
    marginTop:'7.5%',
    resizeMode:'contain',
    zIndex:3,
    alignSelf:'center',
    marginLeft:'2%',
  },
  playing:{
      width:'70%',
      height:'40%',
      elevation:1,
      backgroundColor:'#FFF',
      alignSelf:'center',
      marginTop:'15%',
      borderRadius:20
  }
  
});