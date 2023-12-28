import "./DestinationStyle.css";
import Image1 from "../assets/u5.png"
import Image2 from "../assets/u4.png"
import Image3 from "../assets/u3.jpg"
import Image4 from "../assets/u2.jpg"
import DestinationData from "./DestinationData";

const Destination = () => {
    return ( 
        <div className="destination">
            <h1>What can we here ?</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
            <DestinationData
            className = "first-des"
            heading = "Scanning Your Web Sites"
            text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            img1 = {Image1}
            img2 = {Image2}
            />
            <DestinationData
            className = "first-des-reverse"
            heading = "Find Your Vulnerability"
            text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            img1 = {Image3}
            img2 = {Image4}
            />
        </div>
    )
}
export default Destination;