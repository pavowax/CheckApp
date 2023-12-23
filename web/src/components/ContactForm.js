import "./ContactFormStyle.css"
import React from 'react'

function ContactForm() {
  return (
    <div className="form-container">
        <h1>Send a message to us!</h1>
        <form>
            <input placeholder="Name and Surname"></input>
            <input placeholder="Email"></input>
            <input placeholder="Subject"></input>
            <textarea placeholder="Your Message" rows="4"></textarea>
            <button>Send Message</button>
        </form>
    </div>
  )
}
export default ContactForm;