import React, { Component } from 'react'
import "./NavBarStyles.css"
import { MenuItems } from './MenuItems'
import { Link } from 'react-router-dom'

export default class NavBar extends Component {
    state = {
        clicked : false
    }
    handleClicke = () => {
        this.setState({
            clicked : !this.state.clicked
        })
    }
  render() {
    return (
      <nav className='NavBarItems'>
        <h1 className='navbar-logo'>
            SCANNING APP
        </h1>

        <div className="menu-icons" onClick={this.handleClicke}>
            <i className={this.state.clicked ? "fas fa-times" : "fas fa-bars"}></i>
        </div>

        <ul className={this.state.clicked ? "nav-menu active" : "nav-menu"}>
            {MenuItems.map((item, index) => {
                return (
                <li key={index}>
                <Link className={item.cName} to={item.url}>
                    <i className={item.icon}>{item.title}</i>
                </Link>
            </li>
            )
            })}
            <button>Sign Up</button>
        </ul>
      </nav>
    )
  }
}
