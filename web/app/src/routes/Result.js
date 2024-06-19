import { useLocation, useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import "./result.css"


// Recursive render function
const renderData = (data, level = 0) => {
    if (typeof data === 'object' && data !== null) {
        return (
            <ul style={{ listStyleType: 'none', paddingLeft: `${level * 20}px` }}>
                {Object.keys(data).map((key) => (
                    <TreeItem key={key} itemKey={key} data={data[key]} level={level} />
                ))}
            </ul>
        );
    } else {
        return <span>{String(data)}</span>;
    }
};

function Result() {
    const location = useLocation();
    const navigate = useNavigate();

    const { data } = location.state || {};

    const goToHome = () => {
        navigate('/');
    }

    return (
        <div>
            <div className="container">
                <h1>Result Page</h1>
                <button onClick={goToHome}>Go to Homepage</button>
                {renderData(data)}
            </div>
        </div>
    );
}

// TreeItem component to handle collapsible logic
function TreeItem({ itemKey, data, level }) {
    const [isOpen, setIsOpen] = useState(false);

    const handleToggle = () => {
        setIsOpen(!isOpen);
    };

    return (
        <li>
            <div onClick={handleToggle} style={{ cursor: 'pointer' }}>
                <strong>{itemKey}:</strong> {typeof data === 'object' && data !== null && (isOpen ? '[-]' : '[+]')}
            </div>
            {isOpen && (
                <div>
                    {typeof data === 'object' && data !== null ? renderData(data, level + 1) : <span>{String(data)}</span>}
                </div>
            )}
        </li>
    );
}

export default Result;
