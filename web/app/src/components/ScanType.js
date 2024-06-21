import ScanTypeData from "./ScanTypeData";
import "./ScanTypeStyle.css"
import Image1 from "../assets/x1.png"
import Image2 from "../assets/x2.png"
import Image3 from "../assets/u2.jpg"
//import Image4 from "../assets/u2.jpg"
import React from 'react'

function ScanType() {
  return (
    <div className="scan">
      <h1>SCAN TYPES</h1>
      <p>Various approaches called scanning are employed to find security flaws in websites. Investigating security flaws by direct interaction with target systems is known as active scanning. This technique swiftly detects possible vulnerabilities by addressing target systems with targeted queries and evaluating their responses. Conversely, passive scanning gathers data without interacting with the target systems directly. To find security flaws, it collects information from publicly accessible sources or analyzes network traffic. Reputation scanning assesses websites' dependability and previous security problems. It assists in forecasting potential dangers by looking at past malevolent activity. The combination of these scanning techniques enables thorough assessment of website security flaws and security measure optimization.</p>
      <div className="scanCard"> 
        <ScanTypeData
            image = {Image1}
            heading = "ACTIVE SCANNING"
            text = "It is a proactive method of locating security holes in an online application. Using this technique, requests are sent straight to the target system, where they are analyzed to find potential security flaws. Finding and fixing any vulnerabilities that an attacker could exploit is the most practical and efficient course of action."
        />
        <ScanTypeData
            image = {Image2}
            heading = "PASSIVE SCANNING"
            text = "By examining publicly accessible data, including DNS records, SSL certificates, subdomains, and WHOIS queries, it finds possible vulnerabilities. This technique mimics the manner in which attackers gather system intelligence and enables the detection of security flaws without directly affecting the target system."
        />
        <ScanTypeData
            image = {Image3}
            heading = "REPUTATION SCANNING"
            text = "It is possible for a website server to be compromised and used maliciously. Based on the query results, the site's IP address and domain name are looked up in IOC databases in an effort to increase awareness."
        />
      </div>
    </div>
  )
}
export default ScanType;