import React, { Component } from 'react';
import './Home.css';
import SearchBar from './SearchBar.js';
import UploadImages from './UploadImages.js';
import Model from './Model';

function Home() {
    return (
      <div className="Home">
        <div className="Model">
           <Model /> 
        </div>
        <div className="MainPage">
          <h1 id="main_header">SORT</h1>
          <SearchBar />
          <UploadImages />
        </div>
      </div>
    );
  }
  
  export default Home;
  