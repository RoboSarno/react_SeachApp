import React, { Component } from 'react';
import { CardList } from './components/card-list/card-list.component';
import { SearchBox } from './components/searchBox/search-box.coponenet';
import './App.css';


class App extends Component {

  constructor(){
    super();
    this.state = {
      monsters: [],
      searchField: ''
    };
  }
  //read in the data from url to a users monsters array
  componentDidMount () {
    fetch('https://jsonplaceholder.typicode.com/users')
    .then(response => response.json())
    .then(users => this.setState({ monsters: users }));
  }

  //A good rule of thumb is this: Use arrow functions on any class methods you define and aren't part of React ex: render, componentDidMount
  handleChange = (e) => {
    this.setState({ searchField: e.target.value });
  };

  render() {

    const { monsters, searchField } = this.state;
    const filteredMonsters = monsters.filter(monster => monster.name.toLowerCase().includes(searchField.toLowerCase()));

    return (
      <div className="App">
        <h1>Search Tool</h1>

        <SearchBox placeholder = 'search monster' handleChange ={this.handleChange}/>

        <CardList monsters={filteredMonsters} /> 

      </div>
    );
  }

}


export default App;
