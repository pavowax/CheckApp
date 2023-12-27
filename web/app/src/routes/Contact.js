import React from 'react'
import NavBar from "../components/NavBar"
import Hero from '../components/Hero';
import ContactImg from "../assets/u1.jpg";
import Footer from '../components/Footer';
import ContactForm from '../components/ContactForm';
function Contact() {
  return (
    <>
      <NavBar/>
      <Hero
      cName = "hero-mid"
      heroImg = {ContactImg}
      title = "CONTACT"
      buttonClass = "hide"
      />
      <ContactForm/>
      <Footer/>
    </>
  )
}
export default Contact