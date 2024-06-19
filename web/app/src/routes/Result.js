import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import "./result.css"


function Result() {
    const location = useLocation();
    const navigate = useNavigate();  // history objesini alın

    const { data } = location.state || {};

    // Recursive render function
    const renderData = (data, level = 1) => {
        if (typeof data === 'object' && data !== null) {
            return (
                <ul>
                    {Object.keys(data).map((key, index) => (
                        <li key={key} style={{ "margin-left": `${level * 20}px` }}>
                            <strong>{key}:</strong>
                            {renderData(data[key], level + 1)}
                        </li>
                    ))}
                </ul>
            );
        } else {
            return <span>{String(data)}</span>;
        }
    };

    const goToHome = () => {
        navigate('/');
    }

    return (
        <div className='result'>
            <h1>Result Page</h1>
            <button onClick={goToHome}>Go to Homepage</button>
            {renderData(data)}
        </div>
    );
}

export default Result;
