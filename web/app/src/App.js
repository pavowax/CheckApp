import { Route, Routes } from "react-router-dom"
import "./style.css"
import Home from "./routes/Home";
import About from "./routes/About";
import Service from "./routes/Service";
import Contact from "./routes/Contact";
import Deneme from "./routes/Deneme";
import Sign from "./routes/Sign";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/about" element={<About/>}/>
        <Route path="/service" element={<Service/>}/>
        <Route path="/contact" element={<Contact/>}/>
        <Route path="/sign" element={<Sign/>}/>
        <Route path="/req" element={<Deneme/>}/>
      </Routes>
    </div>
  );
}

export default App;
