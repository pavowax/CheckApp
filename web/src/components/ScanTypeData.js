import "./ScanTypeStyle.css"
import React from 'react'

function ScanTypeData(props) {
  return (
    <div className="s-card">
        <div className="s-img">
            <img src={props.image} alt="img" />
        </div>
        <h3>{props.heading}</h3>
        <p>{props.text}</p>
    </div>
  )
}
export default ScanTypeData;