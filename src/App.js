import React from 'react';
import './App.css';
import background from './images/background.jpg';
import bench from './images/bench.jpg';
import flippedBench from './images/flippedBench.jpg';
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
      playerHighlight: [[false, false, false], [false, false, false], [false, false, false], [false, false, false]],
      enemyHighlight: [[false, false, false], [false, false, false], [false, false, false], [false, false, false]],
      playerWin: 0,
      enemyWin: 0,
      playerPlaceFlag: -1,
      enemyPlaceFlag: -1,
      pieceClickedFirst: "--"
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
    this.setState({playerPlaceFlag: -1});
    this.setState({enemyPlaceFlag: -1});
    this.setState({playerHighlight: [[false, false, false], [false, false, false], [false, false, false], [false, false, false]]});
    this.setState({enemyHighlight: [[false, false, false], [false, false, false], [false, false, false], [false, false, false]]});
    this.setState({pieceClickedFirst: "--"});
  }

  invertCommand(command){ //hardcoded for 2 digit commands
    var first = 3-parseInt(command.substring(0,1))
    var second = 2-parseInt(command.substring(1))
    return first.toString() + second.toString()
  }


  imagePlayerClick(i, j, value){
    var res = i + "" + j;
    command += res;
    console.log(command);

    if(command.length == 2){
      this.setState({pieceClickedFirst: value});
      axios.get('http://localhost:5000/player_valid_space/' + command)
      .then(response => {
        // console.log(response);
        var spaces = response["data"]["valid_space"]
        var highlight = this.state.playerHighlight;
        for (var k = 0; k < spaces.length; k++){
          //prob should check if length = 2 but whatever
          highlight[spaces[k][0]][spaces[k][1]] = true;
        }
        highlight[i][j] = true;
        this.setState({playerHighlight: highlight});
        console.log(highlight);
      })
      .catch(function (error) {
        console.log(error);
      });
    }

    if (command.length == 4){
      if (this.state.pieceClickedFirst.indexOf("M") != -1){
        if (this.state.playerPlaceFlag < 0){
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
        else if (this.state.playerPlaceFlag >= 0){
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
      else{
        if (command.length == 4 && this.state.enemyPlaceFlag < 0){
          axios.get('http://localhost:5000/enemy_move/' + this.invertCommand(command.substring(0,2)) + this.invertCommand(command.substring(2,4)))
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
        else if (command.length == 4 && this.state.enemyPlaceFlag >= 0){
          axios.get('http://localhost:5000/enemy_place/' + command.substring(0,2) + this.invertCommand(command.substring(2,4)))
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
    }
  }

  imageEnemyClick(i, j){
    var res = i + "" + j;
    command += res;
    console.log(command);

    if(command.length == 2){
      axios.get('http://localhost:5000/enemy_valid_space/' + command)
      .then(response => {
        // console.log(response);
        var spaces = response["data"]["valid_space"]
        var highlight = this.state.enemyHighlight;
        for (var k = 0; k < spaces.length; k++){
          //prob should check if length = 2 but whatever
          highlight[spaces[k][0]][spaces[k][1]] = true;
        }
        highlight[i][j] = true;
        this.setState({enemyHighlight: highlight});
        console.log(highlight);
      })
      .catch(function (error) {
        console.log(error);
      });
    }

    if (command.length == 4 && this.state.enemyPlaceFlag < 0){
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
    else if (command.length == 4 && this.state.enemyPlaceFlag >= 0){
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
    this.setState({playerPlaceFlag: i*3+j});
    var res = i + "" + j
    command += res
    console.log(command)

    if(command.length == 2){
      axios.get('http://localhost:5000/player_empty_space/' + command)
      .then(response => {
        // console.log(response);
        var spaces = response["data"]["valid_space"]
        var highlight = this.state.enemyHighlight;
        for (var k = 0; k < spaces.length; k++){
          //prob should check if length = 2 but whatever
          highlight[spaces[k][0]][spaces[k][1]] = true;
        }
        this.setState({playerHighlight: highlight});
        console.log(highlight);
      })
      .catch(function (error) {
        console.log(error);
      });
    }

    if (command.length == 4){
      command = "";
      this.setState({playerPlaceFlag: -1});
      this.setState({playerHighlight: [[false, false, false], [false, false, false], [false, false, false], [false, false, false]]});
      this.setState({enemyPlaceFlag: -1});
      this.setState({enemyHighlight: [[false, false, false], [false, false, false], [false, false, false], [false, false, false]]});
    }
  }

  benchEnemyClick(i, j){
    this.setState({enemyPlaceFlag: i*3+j});
    var res = i + "" + j
    command += res
    console.log(command)

    if(command.length == 2){
      axios.get('http://localhost:5000/enemy_empty_space/' + command)
      .then(response => {
        // console.log(response);
        var spaces = response["data"]["valid_space"]
        var highlight = this.state.playerHighlight;
        for (var k = 0; k < spaces.length; k++){
          //prob should check if length = 2 but whatever
          highlight[3-spaces[k][0]][2-spaces[k][1]] = true;
        }
        this.setState({playerHighlight: highlight});
        console.log(highlight);
      })
      .catch(function (error) {
        console.log(error);
      });
    }

    if (command.length == 4){
      command = "";
      this.setState({enemyPlaceFlag: -1});
      this.setState({playerHighlight: [[false, false, false], [false, false, false], [false, false, false], [false, false, false]]});
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
        if (this.state.playerHighlight[i][j]){
          className += "selected";
        }
        myHTML.push(<button> <img src= {imageMap[array[i][j]]} class= {className} onClick={() => {console.log(this.imagePlayerClick(i, j, array[i][j]))}} /> </button>)
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
        if (this.state.enemyHighlight[i][j]){
          className += "selected";
        }
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
        if (this.state.playerPlaceFlag == i*3+j){
          className += "selected";
        }
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
        if (this.state.enemyPlaceFlag == i*3+j){
          className += "selected";
        }
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
        <div class="wintext">
          {playerWinText}
        </div>
        <img src={flippedBench} class="flippedBench" />
        <div class="flippedBench">
          {enemyBench}
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
    );
    return htmlcode; 
  }
}

export default App;