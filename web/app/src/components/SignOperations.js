import React, { useState } from 'react';
import axios from 'axios';

function SignOperations() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

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
        // const data = response.data.data;
        // const username = JSON.parse(data).Username;
        // localStorage.setItem('username', username)
      }
      console.log(token);
      setIsLoggedIn(true);
      setMessage('Login successful!');
    } catch (error) {
      setMessage('Login failed: Invalid credentials');
    }
  };
  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleLogout = () => {
    localStorage.removeItem('jwt');
    setIsLoggedIn(false);
    setMessage('Logged out');
  };

  const [isActive, setIsActive] = useState(false);
  const handleClick = event => {
    setIsActive(current => !current);
  };

  return (
    <div className='body'>
      <h1>{isLoggedIn ? '' : ''}</h1> {isLoggedIn ? (
        <div>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <section className={isActive ? 'wrapper active' : 'wrapper'}>
          <div className="form signup">
            <header onClick={handleClick}>Signup</header>
            <form>
              <input type="text" placeholder="Username" required />
              <input type="email" placeholder="Email address" required />
              <input type="password" placeholder="Password" required />
              <div className="checkbox">
                <input type="checkbox" id="signupCheck" />
                <label htmlFor="signupCheck">I accept all terms & conditions</label>
              </div>
              <input type="submit" value="Signup" />
            </form>
          </div>
          <div className="form login">
            <header onClick={handleClick}>Login</header>
            <form action='/' >
              <input type="username" placeholder="Username" required value={username} onChange={handleUsernameChange} />
              <input type="password" placeholder="Password" required value={password} onChange={handlePasswordChange} />
              <a href="/">Forgot password?</a>
              <input type="submit" value="Login" className='lognButton' onClick={handleLogin} />

              <input typle="submit" value="Logout" className='lognButton' onClick={handleLogout} />

            </form>
          </div>
        </section>
      )}
      <p>{message}</p>
    </div>
  )
}
export default SignOperations



