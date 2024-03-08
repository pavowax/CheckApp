import React from 'react'
import "./HeroStyle.css"


function Hero(props) {
  
  return (
    <div className={props.cName}>
        <div className='hero-text'>
            <h1>{props.title}</h1>
            <p>
            {props.text}
            </p>
            <hr className='vr'/>
            <form className='search'> 
              <i className="search-icon fa-solid fa-magnifying-glass"></i>
              <input className='search-input' type='text' name='search-bar' id='search-bar'></input> 
              <button className='search-button' type='submit'>Search</button>
            </form>
        </div>
    </div>
    //search barı responsive hale getirilecek!
    //forma method eklenecek
  )
}
export default Hero