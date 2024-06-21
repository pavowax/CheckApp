import { Route, Routes } from "react-router-dom"
import "./style.css"
import Home from "./routes/Home";
import About from "./routes/About";
import Service from "./routes/Service";
import Contact from "./routes/Contact";
import Sign from "./routes/Sign";
import Result from "./routes/Result";


function App() {
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
