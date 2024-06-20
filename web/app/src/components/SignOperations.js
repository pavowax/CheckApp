import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // useHistory hook'unu import edin
import AlertDismissible from './AlertDismissible';


function SignOperations() {

  const [username, setUsername] = useState('');
  const [username1, setUsername1] = useState('');
  const [password, setPassword] = useState('');
  const [password1, setPassword1] = useState('');
  const [phone_number, setPhoneNumber] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();  // history objesini alın
  const [showRegisterAlert, setShowRegisterAlert] = useState(false);
  const [showLoginAlert, setShowLoginAlert] = useState(false);
  const [registerAlertMessage, setRegisterAlertMessage] = useState("Registered failed!");
  const [loginAlertMessage, setLoginAlertMessage] = useState("Login failed!");

  const handleShowRegisterAlert = () => {
    setShowRegisterAlert(true);
  };
  const handleShowLoginAlert = () => {
    setShowLoginAlert(true);
  };

  const handleRegisterAlertClose = () => {
    setShowRegisterAlert(false);
  };

  const handleLoginAlertClose = () => {
    setShowLoginAlert(false);
  };


  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost/api/login', {
        username,
        password
      });
      const token = response.headers.get('Authorization');
      if (token != null) {
        localStorage.setItem('jwt', token);
      }
      console.log(token);
      const Authorization = localStorage.getItem('jwt')
      const config = {
        headers: { Authorization }
      };
      const username1 = await axios.get('http://localhost/api/index', config);
      console.log(username1.data);
      setIsLoggedIn(true);
      navigate('/', { state: { isLoggedIn } });
      // setMessage('Login successful!');
    } catch (error) {
      // setMessage('Login failed: Invalid credentials');
      setLoginAlertMessage(error?.response?.data?.message || "Login failed!")
      handleShowLoginAlert();
    }
  };
  const handleRegister = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost/api/register', {
        username1,
        password1,
        phone_number,
        email
      });
      console.log(response.data)
      if (response.message !== "OK") setRegisterAlertMessage(response?.data?.message || "Registered failed!")
      // setMessage("Succesfully registered!");
    } catch (error) {
      // setMessage("Registered failed!");
      console.log(error)
      setRegisterAlertMessage(error?.response?.data?.message || "Registered failed!");
      handleShowRegisterAlert();
    }
  }
  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };
  const handleUsername1Change = (event) => {
    setUsername1(event.target.value);
  };
  const handlePassword1Change = (event) => {
    setPassword1(event.target.value);
  };
  const handlePhoneNumberChange = (event) => {
    setPhoneNumber(event.target.value);
  };
  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  // const handleLogout = () => {
  //   localStorage.removeItem('jwt');
  //   setIsLoggedIn(false);
  //   setMessage('Logged out');
  // };

  const [isActive, setIsActive] = useState(false);
  const handleClick = () => {
    setIsActive(current => !current);
  };

  return (
    <div className='body'>
      <section className={isActive ? 'wrapper active' : 'wrapper'}>
        <div className="form signup">
          <header onClick={handleClick}>Signup</header>
          <form>
            <input type="text" placeholder="Username" required value={username1} onChange={handleUsername1Change} />
            <input type="email" placeholder="Email address" required value={email} onChange={handleEmailChange} />
            <input type="password" placeholder="Password" required value={password1} onChange={handlePassword1Change} />
            <input type="tel" placeholder="Phone Number" required value={phone_number} onChange={handlePhoneNumberChange} />
            <div className="checkbox">
              <input type="checkbox" id="signupCheck" />
              <label htmlFor="signupCheck">I accept all terms & conditions</label>
            </div>
            <input type="submit" value="Signup" onClick={handleRegister} />
            {showRegisterAlert && (
              <AlertDismissible
                variant="danger"
                heading="Register Error"
                message={registerAlertMessage}
                onClose={handleRegisterAlertClose}
              />
            )}

          </form>
        </div>
        <div className="form login">
          <header onClick={handleClick}>Login</header>
          <form action='/' >
            <input type="username" placeholder="Username" required value={username} onChange={handleUsernameChange} />
            <input type="password" placeholder="Password" required value={password} onChange={handlePasswordChange} />
            <a href="/">Forgot password?</a>
            <input type="submit" value="Login" className='lognButton' onClick={handleLogin} />
            {showLoginAlert && (
              <AlertDismissible
                variant="danger"
                heading="Login Error"
                message={loginAlertMessage}
                onClose={handleLoginAlertClose}
              />
            )}

            {/* <input typle="submit" value="Logout" className='lognButton' onClick={handleLogout} /> */}

          </form>
        </div>
      </section>
      <p>{message}</p>
    </div>
  )
}
export default SignOperations



