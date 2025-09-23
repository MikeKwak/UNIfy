import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import UserInput from "../pages/UserInput";
import RoadMap from "../pages/RoadMap";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/information" element={<UserInput />} />
      <Route path="/roadmap" element={<RoadMap />} />
    </Routes>
  );
}
