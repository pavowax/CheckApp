import React, { Component } from 'react';
import "./NavBarStyles.css";
import { MenuItems } from './MenuItems';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

class NavBar extends Component {

  state = {
    clicked: false,
    username: null,
    isShow: false,
  };

  handleClicke = () => {
    this.setState(prevState => ({ clicked: !prevState.clicked }));
  };

  getUsername = async () => {
    const Authorization = localStorage.getItem('jwt');
    const config = {
      headers: { Authorization }
    };
    try {
      const res = await axios.get('http://localhost/api/index', config);
      const username = JSON.parse(res.data.data.replaceAll(`'`, `"`)).Username;
      console.log(username);
      this.setState({ username });
    } catch (error) {
      console.error('Error fetching username:', error);
    }
  };

  handleClickLogout = () => {
    localStorage.removeItem('jwt');
    const navigate = this.props.navigate;
    navigate('/sign');
  }

  componentDidMount() {
    this.getUsername();
  }

  render() {
    return (
      <nav className='NavBarItems'>
        <h1>
          <a href='/' style={{ textDecoration: "none" }} className='navbar-logo'>CHECKAPP</a>
        </h1>

        <div className="menu-icons" onClick={this.handleClicke}>
          <i className={this.state.clicked ? "fas fa-times" : "fas fa-bars"}></i>
        </div>

        <ul className={this.state.clicked ? "nav-menu active" : "nav-menu"}>
          {MenuItems.map((item, index) => (
            <li key={index}>
              <Link className={item.cName} to={item.url} id={item.id}>
                <i className={item.icon}>{item.title}</i>
              </Link>
            </li>
          ))}
          {this.state.username ? (
            <li key={4}>
              <div className="nav-links" id="username" onClick={() => this.setState(prevState => ({ isShow: !prevState.isShow }))}>
                <i className="fa-solid fa-user"> {this.state.username}</i>
                <ul className={this.state.isShow ? "" : "d-none"}>
                  <li>
                    <div className="nav-links" onClick={this.handleClickLogout} id="logout">
                      <i className="fa-solid fa-user">Logout</i>
                    </div>
                  </li>
                </ul>
              </div>
            </li>
          ) : (
            <li key={4}>
              <Link className="nav-links" to="/sign" id="sign">
                <i className="fa-solid fa-user"> Sign Up</i>
              </Link>
            </li>
          )}
        </ul>
      </nav>
    );
  }
}

export default function WithNavigate(props) {
  const navigate = useNavigate();
  return <NavBar {...props} navigate={navigate} />;
}
