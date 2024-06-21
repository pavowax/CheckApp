import { useState } from 'react';
import Alert from 'react-bootstrap/Alert';

function AlertDismissible({ variant = 'danger', heading = 'Error', message = 'Error message', onClose }) {
    const [show, setShow] = useState(true);

    const handleClose = () => {
        setShow(false);
        if (onClose) {
            onClose();
        }
    };

    if (show) {
        return (
            <Alert variant={variant} onClose={handleClose} dismissible>
                <Alert.Heading>{heading}</Alert.Heading>
                <p>{message}</p>
            </Alert>
        );
    }
    return null;
}

export default AlertDismissible;
