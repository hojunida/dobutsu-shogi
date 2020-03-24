import React from 'react';
import './App.css';
import background from './images/background.jpg';
import bench from './images/bench.jpg';
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

var command = '';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { 
      playerBoard: [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]],
      enemyBoard: [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]],
      playerBench: [["--","--","--"], ["--","--","--"]],
      enemyBench: [["--","--","--"], ["--","--","--"]],
      playerWin: 0,
      enemyWin: 0,
      playerPlaceFlag: false,
      enemyPlaceFlag: false
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

  checkGameFinished(){
    axios.get('http://localhost:5000/player_done')
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.setState({playerWin: response["data"]["done"]});
      })
      .catch(function (error) {
        console.log(error);
      });

      axios.get('http://localhost:5000/enemy_done')
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.setState({enemyWin: response["data"]["done"]});
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  update(response){
    this.setState({playerBoard: response["data"]["playerBoard"]});
    this.setState({enemyBoard: response["data"]["enemyBoard"]});
    this.setState({playerBench: response["data"]["playerBench"]});
    this.setState({enemyBench: response["data"]["enemyBench"]});
    this.setState({playerPlaceFlag: false});
    this.setState({enemyPlaceFlag: false});
  }

  imagePlayerClick(i, j){
    var res = i + "" + j;
    command += res;
    console.log(command);
    if (command.length == 4 && this.state.playerPlaceFlag == false){
      axios.get('http://localhost:5000/player_move/' + command)
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.update(response);
        this.checkGameFinished();
        console.log(this.state.playerBoard);
      })
      .catch(function (error) {
        console.log(error);
      });
      command = "";
    }
    else if (command.length == 4 && this.state.playerPlaceFlag == true){
      axios.get('http://localhost:5000/player_place/' + command)
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.update(response);
        this.checkGameFinished();
        console.log(this.state.playerBoard);
      })
      .catch(function (error) {
        console.log(error);
      });
      command = "";
    }
  }

  imageEnemyClick(i, j){
    var res = i + "" + j;
    command += res;
    console.log(command);
    if (command.length == 4 && this.state.enemyPlaceFlag == false){
      axios.get('http://localhost:5000/enemy_move/' + command)
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.update(response);
        this.checkGameFinished();
        console.log(this.state.playerBoard);
      })
      .catch(function (error) {
        console.log(error);
      });
      command = "";
    }
    else if (command.length == 4 && this.state.enemyPlaceFlag == true){
      axios.get('http://localhost:5000/enemy_place/' + command)
      .then(response => {
        console.log(response);
        // this.forceUpdate();
        this.update(response);
        this.checkGameFinished();
        console.log(this.state.playerBoard);
      })
      .catch(function (error) {
        console.log(error);
      });
      command = "";
    }
  }

  benchPlayerClick(i, j){
    this.setState({playerPlaceFlag: true});
    var res = i + "" + j
    command += res
    console.log(command)
    if (command.length == 4){
      command = "";
    }
  }

  benchEnemyClick(i, j){
    this.setState({enemyPlaceFlag: true});
    var res = i + "" + j
    command += res
    console.log(command)
    if (command.length == 4){
      command = "";
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
        myHTML.push(<button> <img src= {imageMap[array[i][j]]} class= {className} onClick={() => {console.log(this.imagePlayerClick(i, j))}} /> </button>)
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
        myHTML.push(<button> <img src= {imageMap[array[i][j]]} class= {className} onClick={() => {console.log(this.imageEnemyClick(i, j))}} /> </button>)
      }
    }
    return myHTML
  }

  playerBenchHTMLCode(array){
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
        myHTML.push(<button> <img src= {imageMap[array[i][j]]} class= {className} onClick={() => {console.log(this.benchPlayerClick(i, j))}} /> </button>)
      }
    }
    return myHTML
  }


  enemyBenchHTMLCode(array){
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
        myHTML.push(<button> <img src= {imageMap[array[i][j]]} class= {className} onClick={() => {console.log(this.benchEnemyClick(i, j))}} /> </button>)
      }
    }
    return myHTML
  }

  render() {

    var playerImages = this.imagePlayerHTMLCode(this.state.playerBoard);
    var enemyImages = this.imageEnemyHTMLCode(this.state.enemyBoard);

    var playerBench = this.playerBenchHTMLCode(this.state.playerBench);
    var enemyBench = this.enemyBenchHTMLCode(this.state.enemyBench);


    let playerWinTextArray = ["", "PLAYER 1 WINS", "GAME DRAWN"]

    let enemyWinTextArray = ["", "PLAYER 2 WINS", "GAME DRAWN"]

    var playerWinText = playerWinTextArray[this.state.playerWin]
    var enemyWinText = enemyWinTextArray[this.state.enemyWin]

    var htmlcode = (
      <div>
        <div class="split left">
          <div class="wintext">
            {playerWinText}
          </div>
          <img src={background} class="background" />
          <div class="board">
           {playerImages}
          </div>
          <img src={bench} class="bench" />
          <div class="bench">
            {playerBench}
          </div>
        </div>

        <div class= "split right">
          <div class="wintext">
            {enemyWinText}
          </div>
          <img src={background} class="background" />        
          <div class="board">        
            {enemyImages}
          </div>
          <img src={bench} class="bench" />
          <div class="bench">
            {enemyBench}
          </div>
        </div>
      </div>
    );
    return htmlcode; 
  }
}

export default App;