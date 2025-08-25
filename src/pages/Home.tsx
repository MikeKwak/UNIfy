import { Link } from "react-router-dom";
import NavBar from "../components/NavBar";

export default function Home() {
  return (
    <div className="bg-white text-black font-sans">
      {/* Navbar */}
      <NavBar />

      {/* Hero Section */}
      <section className="flex flex-col-reverse md:flex-row items-center justify-center min-h-screen max-w-7xl mx-auto px-6">
        {/* Text */}
        <div className="max-w-3xl text-center md:text-left px-6">
          <h1 className="text-5xl md:text-7xl mb-6">
            A personalized path to your dream university.
          </h1>
          <p className="text-lg mb-8 text-gray-700">
            Making university admissions accessible for all, one step at a time
          </p>
          <Link
            to="/login"
            className="bg-lime-500 hover:bg-lime-600 text-black px-6 py-3 rounded shadow-md font-semibold transition"
          >
            Get Started
          </Link>
        </div>

        {/* Image */}
        <div className="md:w-1/2 mb-12 md:mb-0 flex justify-center">
          <img
            src="/logo.svg"
            alt="Graduation Book"
            className="w-full max-w-xl mx-auto"
          />
        </div>
      </section>
    </div>
  );
}
