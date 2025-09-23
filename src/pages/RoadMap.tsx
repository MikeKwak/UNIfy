import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";

export default function RoadMap() {
  const navigate = useNavigate();

  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Nav bar */}
      <NavBar />

      {/* Body */}
      <main className="pt-36 md:pt-40 pb-16 px-4 max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-10 items-start">
          {/* Hero Section */}
          <section>
            <h1 className="text-[34px] leading-[1.1] sm:text-5xl md:text-6xl font-normal tracking-tight">
              Your step‑by‑step plan for ___ University
            </h1>
            <p className="mt-6 text-[18px] sm:text-xl leading-6 sm:leading-7 tracking-[-0.02em] text-black">
              Click on each Checkpoint for more details.
            </p>
            <div className="mt-10 inline-flex items-center justify-between w-full sm:w-auto gap-4 rounded-[15px] px-5 py-3 text-[18px] sm:text-xl tracking-[-0.02em] ring-1 ring-gray-200 hover:ring-gray-300 transition">
              See my other university recommendations
              <button
                onClick={() => navigate("/recommendations")}
                className="inline-flex h-8 w-20 sm:w-32 items-center justify-center rounded-[15px] bg-[#92BD3A] text-black hover:bg-lime-600"
              >
                →
              </button>
            </div>
          </section>
          {/* Roadmap Image */}
          <img
            src="/roadmap.svg"
            alt="Roadmap"
            className="absolute bottom-0 right-0 max-h-full max-w-full object-contain
                 z-0 pointer-events-none select-none"
          />
        </div>
      </main>
    </div>
  );
}
