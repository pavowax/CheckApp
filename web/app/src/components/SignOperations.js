import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import AlertDismissible from './AlertDismissible';


function SignOperations() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [phone_number, setPhoneNumber] = useState('');
  const [email, setEmail] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const [showRegisterAlert, setShowRegisterAlert] = useState(false);
  const [showLoginAlert, setShowLoginAlert] = useState(false);
  const [registerAlertMessage, setRegisterAlertMessage] = useState("Registered failed!");
  const [registerAlertVariant, setRegisterAlertVariant] = useState("danger");
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
    } catch (error) {
      setLoginAlertMessage(error?.response?.data?.message || "Login failed!")
      handleShowLoginAlert();
    }
  };
  const handleRegister = async (event) => {
    event.preventDefault();

    const token = localStorage.getItem('jwt');
    if (token) {
      setRegisterAlertVariant("danger")
      setRegisterAlertMessage("Already logged in!")
      handleShowRegisterAlert();
      return;
    }

    try {
      const response = await axios.post('http://localhost/api/register', {
        username,
        password,
        email,
        phone_number,
      });
      console.log(response.data)
      if (response.data.message === "OK") {
        setRegisterAlertVariant("success")
        setRegisterAlertMessage("Succesfully Registered!")
        window.location.reload();
      }
      else {

        setRegisterAlertVariant("danger")
        setRegisterAlertMessage(response?.data?.message || "Registered failed!")
      }

      handleShowRegisterAlert();
    } catch (error) {
      console.log(error)
      setRegisterAlertVariant("danger")
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
    setUsername(event.target.value);
  };
  const handlePassword1Change = (event) => {
    setPassword(event.target.value);
  };
  const handlePhoneNumberChange = (event) => {
    setPhoneNumber(event.target.value);
  };
  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };


  const [isActive, setIsActive] = useState(false);
  const handleClick = () => {
    setIsActive(current => !current);
  };

  const goToHome = () => {
    navigate('/');
  };

  return (
    <div className='body'>
      <button className="button" onClick={goToHome}>Go to Homepage</button>
      <section className={isActive ? 'wrapper active' : 'wrapper'}>
        <div className="form signup">
          <header onClick={handleClick}>Signup</header>
          <form>
            <input type="text" placeholder="Username" value={username} onChange={handleUsername1Change} />
            <input type="email" placeholder="Email address" value={email} onChange={handleEmailChange} />
            <input type="tel" placeholder="Phone Number" value={phone_number} onChange={handlePhoneNumberChange} />
            <input type="password" placeholder="Password" value={password} onChange={handlePassword1Change} />
            <div className="checkbox">
              <input type="checkbox" id="signupCheck" />
              <label htmlFor="signupCheck">I accept all terms & conditions</label>
            </div>
            <input type="submit" value="Signup" onClick={handleRegister} />
            {showRegisterAlert && (
              <AlertDismissible
                variant={registerAlertVariant}
                heading="Register Message"
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
          </form>
        </div>
      </section>
    </div>
  )
}
export default SignOperations



