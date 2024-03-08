import React from 'react'
import NavBar from "../components/NavBar"
import Hero from '../components/Hero';
import Footer from '../components/Footer';
import ContactForm from '../components/ContactForm';
function Contact() {
  return (
    <>
      <NavBar/>
      <Hero
      cName = "hero-mid"
      title = "CONTACT"
      />
      <ContactForm/>
      <Footer/>
    </>
  )
}
export default Contact