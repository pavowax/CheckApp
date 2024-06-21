import { useLocation, useNavigate } from 'react-router-dom';
import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import 'bootstrap/dist/css/bootstrap.min.css';
import './result.css';

// Recursive render function
const renderData = (data, level = 0) => {
    // if (data === null || data === "null") { data = "*** Secret Information ***"; return (<span>{data}</span>) }
    if (typeof data === 'object' && data !== null) {
        if (Array.isArray(data) && !data.length) { data = "*** Secret Information (Array) ***"; return (<span>{data}</span>) }
        return (
            <Accordion>
                {Object.keys(data).map((key, index) => (
                    <TreeItem
                        index={`${level}-${index}`}
                        key={`${level}-${index}`}
                        itemKey={key}
                        data={data[key]}
                        level={level}
                    />
                ))}
            </Accordion>
        );
    } else {
        return <span>{String(data)}</span>;
    }
};

// TreeItem component to handle collapsible logic
function TreeItem({ index, itemKey, data, level }) {
    return (
        <Accordion.Item eventKey={index}>
            <Accordion.Header>{itemKey}</Accordion.Header>
            <Accordion.Body>
                {typeof data === 'object' && data !== null ? renderData(data, level + 1) : <span>{String(data)}</span>}
            </Accordion.Body>
        </Accordion.Item>
    );
}

function Result() {
    const location = useLocation();
    const navigate = useNavigate();

    const { data } = location.state || {};

    const goToHome = () => {
        navigate('/');
    };

    return (
        <div className="result">
            <h1>Result Page</h1>
            <button className="button" onClick={goToHome}>Go to Homepage</button>
            {data ? renderData(data) : <p>No data available</p>}
        </div>
    );
}

export default Result;
