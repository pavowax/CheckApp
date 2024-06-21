import "./FooterStyle.css";

const Footer = () => {
    return(
        <div className="footer">
            <div className="top">
                <div>
                    <h1>CHECKAPP</h1>
                    <hr></hr>
                    <p>CheckApp is a dependable and easy-to-use software program that can find possible security holes in webpages. In order to find vulnerabilities, this program uses both passive and active scanning techniques, which involve examining network traffic and sending direct queries to target systems.<br></br>CheckApp's sophisticated vulnerability scanning algorithms and security testing methodologies allow it to simulate a variety of attack routes in order to thoroughly assess the security posture of websites. Users can prioritize security vulnerabilities based on severity and evaluate scan results in full reports.</p>
                <hr></hr>
                </div>
                <div>
                    <a href="/">
                        <i className="fa-brands fa-facebook-square"></i>
                    </a>
                    <a href="/">
                        <i className="fa-brands fa-instagram-square"></i>
                    </a>
                    <a href="/">
                        <i className="fa-brands fa-github-square"></i>
                    </a>
                    <a href="/">
                        <i className="fa-brands fa-twitter-square"></i>
                    </a>
                </div>
            </div>
            <div className="bottom">
                <div>
                    <h4><ins>Project</ins></h4>
                    <a href="/">ChangeLog</a>
                    <a href="/">Status</a>
                    <a href="/">License</a>
                    <a href="/">All Versions</a>
                </div>
                <div>
                    <h4><ins>Community</ins></h4>
                    <a href="/">Github</a>
                    <a href="/">Issues</a>
                    <a href="/">Project</a>
                    <a href="/">Twitter</a>
                </div>
                <div>
                    <h4><ins>Help</ins></h4>
                    <a href="/">Support</a>
                    <a href="/">TroubleSgooting</a>
                    <a href="/">Contact Us</a>
                    <a href="/">FAQ</a>
                </div>
                <div>
                    <h4><ins>Others</ins></h4>
                    <a href="/">Terms of Service</a>
                    <a href="/">Privacy Policy</a>
                    <a href="/">License</a>
                </div>
            </div>
        </div>
    )
}
export default Footer;