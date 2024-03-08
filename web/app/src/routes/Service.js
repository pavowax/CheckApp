import React from 'react'
import NavBar from "../components/NavBar"
import Hero from '../components/Hero';
import Footer from '../components/Footer';
import ScanType from '../components/ScanType';
function Service() {
  return (
    <>
      <NavBar/>
      <Hero
      cName = "hero-mid"
      title = "SERVİCE"
      />
      <ScanType/>
      <Footer/>
    </>
  )
}
export default Service