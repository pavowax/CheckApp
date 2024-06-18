import { useEffect } from "react"
import { Route, Routes, useLocation, useHistory } from "react-router-dom"
import "./style.css"
import Home from "./routes/Home";
import About from "./routes/About";
import Service from "./routes/Service";
import Contact from "./routes/Contact";
import Sign from "./routes/Sign";
import Result from "./routes/Result";


function App() {
  // const history = useHistory();
  // const location = useLocation();

  // useEffect(() => {
  //   console.log('Current route:', location.pathname);
  //   const token = localStorage.getItem('jwt');
  //   if (!token) {
  //     // history.push('/sign');
  //   }
  // }, [location]);

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/service" element={<Service />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/sign" element={<Sign />} />      
        <Route path="/result" element={<Result />} />
        
      </Routes>
    </div>
  );
}

export default App;
