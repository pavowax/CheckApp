import "./DestinationStyle.css";
import Image1 from "../assets/u1.png"
import Image2 from "../assets/u2.png"
import Image3 from "../assets/u3.jpg"
import Image4 from "../assets/u3.png"
import DestinationData from "./DestinationData";

const Destination = () => {
    return ( 
        <div className="destination">
            <h1>What can we here ?</h1>
            <p>This application uses active, passive, and reputation scanning techniques to efficiently find security flaws in websites. With the active scanning method, you may quickly identify potential vulnerabilities by engaging directly with target systems and doing in-depth security studies. By keeping an eye on network activity and obtaining information from open sources, the passive scanning approach finds vulnerabilities without causing any disruptions to the system. Reputation scanning assesses websites' dependability and previous security events to help you foresee potential threats. This makes it possible for you to quickly find security holes in your website and take the appropriate action to make it as secure as possible. Furthermore, you can swiftly design remedies and analyze detected vulnerabilities with ease because to the user-friendly reporting capabilities.</p>
            <DestinationData
            className = "first-des"
            heading = "Scanning Your Web Sites"
            text = "You can use active, passive, and reputation scanning techniques to conduct thorough scans with this tool to find security flaws in websites. By interacting directly with target systems, the active scanning method may quickly detect potential vulnerabilities and do detailed security studies. In order to covertly find vulnerabilities, passive scanning lets you keep an eye on network activity and collect data from open sources without interfering with the system. Reputation scanning assesses websites' dependability and past security problems to help you foresee potential threats. With the help of these integrated techniques, you can do thorough and effective scans, giving your website the highest level of security possible."
            img1 = {Image1}
            img2 = {Image2}
            />
            <DestinationData
            className = "first-des-reverse"
            heading = "Find Your Vulnerability"
            text = "This tool is capable of effectively identifying vulnerabilities in websites using various scanning methods such as active, passive, and reputation scanning. Active scanning involves direct interaction with target systems to conduct comprehensive security assessments, enabling quick discovery of potential vulnerabilities. Passive scanning operates by monitoring network traffic and collecting data from public sources without actively engaging with the system, thus identifying vulnerabilities in a non-intrusive manner. Reputation scanning assesses the historical security posture and reliability of websites, aiding in the prediction and mitigation of future threats. Together, these methods empower users to identify and address vulnerabilities promptly, enhancing overall website security and resilience against cyber threats."
            img1 = {Image3}
            img2 = {Image4}
            />
        </div>
    )
}
export default Destination;