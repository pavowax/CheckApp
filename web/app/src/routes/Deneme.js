import React, { useState, useEffect } from "react";

  
function Deneme() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://localhost/api")
      .then((res) => res.json())
      .then((data) => setMessage(data.message));
  }, []);
  return (
    <div>
      Temp = {message}
    </div>
  )
}
export default Deneme