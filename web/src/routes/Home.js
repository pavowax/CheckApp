import React from 'react'
import NavBar from "../components/NavBar"
import Hero from '../components/Hero';
import HomeImg from "../assets/u1.jpg";
import Destination from "../components/Destination"
import ScanType from '../components/ScanType';
import Footer from '../components/Footer';
function Home() {
  return (
    <>
      <NavBar/>
      <Hero
      cName = "hero"
      heroImg = {HomeImg}
      title = "SECURITY"
      text = "Take the your secure for attacks"
      buttonText = "Scanning Type"
      url = "/"
      buttonClass = "show"
      />
      <Destination/>
      <ScanType/>
      <Footer/>
    </>
  )
}
export default Home;