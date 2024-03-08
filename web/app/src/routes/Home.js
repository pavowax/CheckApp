import React from 'react'
import NavBar from "../components/NavBar"
import Hero from '../components/Hero';
import Destination from "../components/Destination"
import ScanType from '../components/ScanType';
import Footer from '../components/Footer';
function Home() {
  return (
    <>
      <NavBar/>
      <Hero
      cName = "hero"
      title = "SECURITY"
      text = "Take the your secure for attack" //Cümlenin devamı için ortalama yapılacak..
      />
      <Destination/>
      <ScanType/>
      <Footer/>
    </>
  )
}
export default Home;