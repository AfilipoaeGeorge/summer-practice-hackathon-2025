import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/users/")
      .then(response => {
        console.log(response.data);
        setMessage(JSON.stringify(response.data));
      })
      .catch(error => {
        setMessage("Error fetching data");
        console.error(error);
      });
  }, []);  

  return (
    <div>
      <h1>GitGud Frontend</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
