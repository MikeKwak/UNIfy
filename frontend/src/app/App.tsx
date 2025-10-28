import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import UserInput from "../pages/UserInput";
import RoadMap from "../pages/RoadMap";
import Recommendations from "../pages/Recommendations";
import Eligibility from "../pages/Eligibility";
import RequiredDocs from "../pages/RequiredDocs";
import Submission from "../pages/Submissions";
import Signup from "../pages/signup";
import ProtectedRoute from "../components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/information" element={<ProtectedRoute><UserInput /></ProtectedRoute>} />
      <Route path="/roadmap" element={<ProtectedRoute><RoadMap /></ProtectedRoute>} />
      <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
      <Route path="/eligibility" element={<ProtectedRoute><Eligibility /></ProtectedRoute>} />
      <Route path="/required" element={<ProtectedRoute><RequiredDocs /></ProtectedRoute>} />
      <Route path="/submission" element={<ProtectedRoute><Submission /></ProtectedRoute>} />
    </Routes>
  );
}
