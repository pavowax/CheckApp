import React from 'react'
import NavBar from "../components/NavBar"
import Hero from '../components/Hero';
import Footer from '../components/Footer';
import AboutUs from '../components/AboutUs';
function About() {
  return (
    <>
      <NavBar/>
      <Hero
      cName = "hero-mid"
      title = "ABOUT"
      />
      <AboutUs/>
      <Footer/>
    </>
  )
}
export default About