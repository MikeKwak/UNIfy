import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import AccessibilityMenu from "./AccessibilityMenu";
import logoSvg from "../assets/logo.svg";

export default function NavBar() {
  const [open, setOpen] = useState(false);
  const { isAuthenticated, user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await signOut();
      navigate("/");
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <>
      <nav className="w-full px-6 py-4 shadow-md bg-white fixed top-0 left-0 z-50">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <img src={logoSvg} alt="Logo" className="h-12 w-12" />
            <Link to="/" className="font-bold text-xl">
              UNIfy
            </Link>
          </div>

          <div className="flex items-center space-x-8">
            {/* Nav Links */}
            <ul className="hidden md:flex space-x-8 text-sm font-medium">
              <li>
                <Link to="/about" className="hover:text-gray-500">
                  About us
                </Link>
              </li>
              <li>
                <Link to="/services" className="hover:text-gray-500">
                  Services
                </Link>
              </li>
              <li>
                <Link to="/updates" className="hover:text-gray-500">
                  Updates
                </Link>
              </li>
            </ul>

            {/* Auth Section */}
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-600">
                    Welcome, {user?.email || user?.username}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-4">
                  <Link
                    to="/login"
                    className="text-sm font-medium text-gray-700 hover:text-gray-500"
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="bg-lime-500 hover:bg-lime-600 text-white px-4 py-2 rounded-md text-sm font-medium transition"
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </div>

            {/* Hamburger Menu */}
            <div className="cursor-pointer" onClick={() => setOpen(!open)}>
              <div className="space-y-1">
                <div className="w-7 h-0.5 bg-black"></div>
                <div className="w-7 h-0.5 bg-black"></div>
                <div className="w-7 h-0.5 bg-black"></div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Accessibility Menu */}
      <AccessibilityMenu open={open} onClose={() => setOpen(false)} />
    </>
  );
}
