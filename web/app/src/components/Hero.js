import React, { useState } from 'react'
import "./HeroStyle.css"
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // useHistory hook'unu import edin



function Hero(props) {
  const [address, setAddress] = useState('');
  const [parameters, setParameters] = useState('');
  const [active, setActive] = useState(false);
  const [passive, setPassive] = useState(false);
  const [reputation, setReputation] = useState(false);

  const [loading, setLoading] = useState(false);  // Overlay kontrolü için yeni state
  const navigate = useNavigate();  // history objesini alın


  const handleSubmit = async (event) => {
    event.preventDefault();

    const parametersArray = parameters.split(',').map(param => param.trim())
    const sendData = {
      address,
      parameters: parametersArray,
      active,
      passive,
      reputation
    }
    const Authorization = localStorage.getItem('jwt')
    const config = {
      headers: { Authorization }
    };

    console.log(sendData)
    setLoading(true);  // Overlay'i göster

    try {
      const response = await axios.post('http://localhost/api/scanner', sendData, config);
      const data = response.data.data.replaceAll(`'`, `"`).replaceAll("None", "null").replaceAll(`"null"`, "null").replaceAll("null", `"*** Secret ***"`).replaceAll("True", "true").replaceAll("False", "false");
      console.log(data);
      window.kerem = data;
      const parsedData = JSON.parse(data);
      const styledData = Object.keys(parsedData).reduce((acc, key) => {
        if (key.includes("reputation_")) acc.reputation = { ...acc.reputation, [key]: parsedData[key] }
        else if (key.includes("passive_")) acc.passive = { ...acc.passive, [key]: parsedData[key] }
        else acc.active = { ...acc.active, [key]: parsedData[key] }
        return acc;
      }, { active: {}, passive: {}, reputation: {} });

      if (response.data.message === 'OK') {
        // Yanıt alındıktan sonra Result sayfasına yönlendirme yapın
        navigate('/result', { state: { data: styledData } });
      }
      else
        alert("Not found!")
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);  // Overlay'i kaldır
    }

  };

  const handleAddressChange = (event) => {
    setAddress(event.target.value);
  };
  const handleParametersChange = (event) => {
    setParameters(event.target.value);
  };
  const handleActiveChange = (event) => {
    setActive(event.target.checked);
  };
  const handlePassiveChange = (event) => {
    setPassive(event.target.checked);
  };
  const handleReputationChange = (event) => {
    setReputation(event.target.checked);
  };

  return (
    <div className={props.cName}>
      {loading && <div className="overlay">Loading...</div>}
      <div className='hero-text'>
        <h1>{props.title}</h1>
        <p>
          {props.text}
        </p>
        <hr className='vr' />
        <form className='search' onSubmit={handleSubmit}>
          <i className="search-icon fa-solid fa-magnifying-glass"></i>
          <input className='search-input' type='text' name='search-bar' id='search-bar' value={address} onChange={handleAddressChange} />
          <input className='search-input-2' type='text' name='search-bar-2' id='search-bar-2' value={parameters} onChange={handleParametersChange} />
          <input className="active-checkbox" id="active-checkbox" type="checkbox" checked={active} onChange={handleActiveChange} /><label className="active-checkbox" for="active-checkbox">Active</label>
          <input className="passive-checkbox" id="passive-checkbox" type="checkbox" checked={passive} onChange={handlePassiveChange} /><label className="passive-checkbox" for="passive-checkbox">Passive</label>
          <input className="reputation-checkbox" id="reputation-checkbox" type="checkbox" checked={reputation} onChange={handleReputationChange} /><label className="reputation-checkbox" for="reputation-checkbox">Reputation</label>
          <button className='search-button' type='submit'>Search</button>
        </form>
      </div>
    </div>
    //search barı responsive hale getirilecek!
    //forma method eklenecek
  )
}
export default Hero