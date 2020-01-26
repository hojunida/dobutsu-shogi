import React from 'react';
import './App.css';
import background from './images/background.jpg';
import ML from './images/ML.jpg';
import MH from './images/MH.jpg';
import MC from './images/MC.jpg';
import ME from './images/ME.jpg';
import MG from './images/MG.jpg';
import EL from './images/EL.jpg';
import EH from './images/EH.jpg';
import EC from './images/EC.jpg';
import EE from './images/EE.jpg';
import EG from './images/EG.jpg';
import TP from './images/TP.png';
import $ from 'jquery';
import axios from 'axios';

var state = '';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { 
      playerBoard: [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]],
      enemyBoard: [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]]
    };
    this.resetBoard();
    // this.imageClick = this.imageClick.bind();
  }

  resetBoard(){
      return axios.get('http://localhost:5000/reset')
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  imagePlayerClick(i, j){
    var res = i + "" + j
    state += res
    console.log(state)
    if (state.length == 4){
      axios.get('http://localhost:5000/player_move/' + state)
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.setState({playerBoard: response["data"]["board"]});
        this.setState({enemyBoard: response["data"]["enemy"]});
        console.log(this.state.playerBoard);
      })
      .catch(function (error) {
        console.log(error);
      });
      state = "";
    }
  }

  imageEnemyClick(i, j){
    var res = i + "" + j
    state += res
    console.log(state)
    if (state.length == 4){
      axios.get('http://localhost:5000/enemy_move/' + state)
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.setState({enemyBoard: response["data"]["board"]});
        this.setState({playerBoard: response["data"]["enemy"]});
        console.log(this.state.playerBoard);
      })
      .catch(function (error) {
        console.log(error);
      });
      state = "";
    }
  }

  getClass(a,b){
    var row = {0:"a", 1:"b", 2:"c"};
    return 'piece'+row[b]+(a+1);
  }

  imagePlayerHTMLCode(array){
    var imageMap = {
      "EG": EG,
      "EL": EL,
      "EE": EE,
      "EC": EC,
      "EH": EH,
      "MG": MG,
      "ML": ML,
      "ME": ME,
      "MC": MC,
      "MH": MH,
      "--": TP
    }
    var myHTML = [];

    for (let i = 0; i < array.length; i++){
      for (let j = 0; j < array[0].length; j++){
        var className = this.getClass(i,j);
        myHTML.push(<button> <img src= {imageMap[array[i][j]]} class= {className} onClick={() => {console.log(this.imagePlayerClick(i, j))}} /> </button>) //comment to fix syntax
      }
    }
    return myHTML
  }

  imageEnemyHTMLCode(array){
    var imageMap = {
      "EG": EG,
      "EL": EL,
      "EE": EE,
      "EC": EC,
      "EH": EH,
      "MG": MG,
      "ML": ML,
      "ME": ME,
      "MC": MC,
      "MH": MH,
      "--": TP
    }
    var myHTML = [];

    for (let i = 0; i < array.length; i++){
      for (let j = 0; j < array[0].length; j++){
        var className = this.getClass(i,j);
        myHTML.push(<button> <img src= {imageMap[array[i][j]]} class= {className} onClick={() => {console.log(this.imageEnemyClick(i, j))}} /> </button>) //comment to fix syntax
      }
    }
    return myHTML
  }

  render() {

    var playerImages = this.imagePlayerHTMLCode(this.state.playerBoard);
    var enemyImages = this.imageEnemyHTMLCode(this.state.enemyBoard);

    var htmlcode = (
      <div>
        <div class="split left">
          <img src={background} class="background" />
          <div class="board">
           {playerImages}
          </div>
        </div>

        <div class= "split right">
          <img src={background} class="background" />        
          <div class="board">        
            {enemyImages}
          </div>
        </div>
      </div>
    );
    return htmlcode; 
  }
}

export default App;