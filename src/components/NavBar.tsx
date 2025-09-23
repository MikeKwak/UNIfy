import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav className="w-full px-6 py-4 shadow-md bg-white fixed top-0 left-0 z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <img src="/logo.svg" alt="Logo" className="h-12 w-12" />
          <Link to="/" className="font-bold text-xl">UNIfy</Link>
        </div>

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

        {/* Hamburger Menu (not functional yet) */}
        <div className="md:hidden">
          <div className="space-y-1">
            <div className="w-6 h-0.5 bg-black"></div>
            <div className="w-6 h-0.5 bg-black"></div>
            <div className="w-6 h-0.5 bg-black"></div>
          </div>
        </div>
      </div>
    </nav>
  );
}
