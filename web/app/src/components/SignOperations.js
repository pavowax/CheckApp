import React, { useState } from 'react';

function SignOperations() {
    const [isActive, setIsActive] = useState(false);
        const handleClick = event => {
            setIsActive(current => !current);
    };
    return(
        <div className='body'>
            <section className={isActive ? 'wrapper active' : 'wrapper'}>
                <div className="form signup">
                    <header onClick={handleClick}>Signup</header>
                    <form action="/">
                        <input type="text" placeholder="Full name" required />
                        <input type="email" placeholder="Email address" required />
                        <input type="password" placeholder="Password" required />
                        <div className="checkbox">
                            <input type="checkbox" id="signupCheck" />
                            <label htmlFor="signupCheck">I accept all terms & conditions</label>
                        </div>
                        <input type="submit" value="Signup" />
                    </form>
                </div>
                <div className="form login">
                    <header onClick={handleClick}>Login</header>
                    <form action="/">
                        <input type="email" placeholder="Email address" required />
                        <input type="password" placeholder="Password" required />
                        <a href="/">Forgot password?</a>
                        <input type="submit" value="Login" className='lognButton'/>
                    </form>
                </div>
            </section>
        </div>
    )
}
export default SignOperations



    