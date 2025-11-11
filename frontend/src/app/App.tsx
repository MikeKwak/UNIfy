import { Routes, Route , useLocation} from "react-router-dom";
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
import About from "../pages/About";
import { FontSizeProvider } from "../../fonts/FontSizeContext";
import  Layout  from "../../fonts/Layout";

export default function App() {
  const location = useLocation();
  return (
    <FontSizeProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login key={location.key}/>} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/information" element={<ProtectedRoute><UserInput /></ProtectedRoute>} />
          <Route path="/roadmap" element={<ProtectedRoute><RoadMap /></ProtectedRoute>} />
          <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
          <Route path="/eligibility" element={<ProtectedRoute><Eligibility /></ProtectedRoute>} />
          <Route path="/required" element={<ProtectedRoute><RequiredDocs /></ProtectedRoute>} />
          <Route path="/submission" element={<ProtectedRoute><Submission /></ProtectedRoute>} />
        </Routes>
      </Layout>
    </FontSizeProvider>
  );
}
