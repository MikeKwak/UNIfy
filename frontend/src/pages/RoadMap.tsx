import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import { getRoadmapSVG, getGeminiRecommendations } from "../services/api";
import type { RecommendationResponse, StudentProfile } from "../services/api";


interface RoadmapData {
  studentProfile: StudentProfile;
  recommendations: RecommendationResponse;
}


export default function RoadMap() {
  const navigate = useNavigate();
  const [roadmapData, setRoadmapData] = useState<RoadmapData | null>(null);
  const [loading, setLoading] = useState(true);
  const [svg, setSvg] = useState<string | null>(null);
  const [university, setUniversity] = useState<string>("Your University");

  useEffect(() => {
    async function fetchRoadmap() {
      const storedData = sessionStorage.getItem('roadmapData');
      let universityName = "Your University";
      const defaultSteps: string[] = [
        "Eligibility & Prerequisites",
        "Required Documents",
        "Application Submission",
        "Decision & Next Steps"
      ];
      if (storedData) {
        try {
          const parsedData: RoadmapData = JSON.parse(storedData);
          setRoadmapData(parsedData);
          const geminiResult = await getGeminiRecommendations(parsedData.studentProfile);
          universityName = geminiResult.recommendations?.[0]?.name || universityName;
          setUniversity(universityName);
          const geminiSteps = geminiResult.recommendations?.map((rec) => rec.name) || defaultSteps;
          const svgData = await getRoadmapSVG({ university: universityName, steps: geminiSteps });
          setSvg(svgData);
        } catch (error) {
          console.error('Error parsing roadmap data or fetching Gemini:', error);
          setRoadmapData(null); // Show fallback UI instead of redirect
          setSvg(null);
          setUniversity("Your University");
        }
      } else {
        setRoadmapData(null); // Show fallback UI instead of redirect
        setSvg(null);
        setUniversity("Your University");
      }
      setLoading(false);
    }
    fetchRoadmap();
  }, [navigate]);

  if (loading) {
    return (
      <div className="font-blmelody bg-white text-gray-900 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-lime-600 mx-auto mb-4"></div>
          <p>Loading your roadmap...</p>
        </div>
      </div>
    );
  }

  if (!roadmapData) {
    return (
      <div className="font-blmelody bg-white text-gray-900 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p>No roadmap data available. Please generate a new roadmap.</p>
          <button 
            onClick={() => navigate('/information')}
            className="mt-4 bg-lime-500 hover:bg-lime-600 text-white px-6 py-2 rounded-md"
          >
            Generate Roadmap
          </button>
        </div>
      </div>
    );
  }

  const { recommendations } = roadmapData;

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
              Your step‑by‑step plan for {svg ? university : "___"} University
            </h1>
            <p className="mt-6 text-[18px] sm:text-xl leading-6 sm:leading-7 tracking-[-0.02em] text-black">
              Click on each Checkpoint for more details.
            </p>
            {/* Source Information */}
            <div className="mt-6 p-4 bg-lime-50 border border-lime-200 rounded-lg">
              <p className="text-sm text-lime-800">
                <strong>Recommendation Source:</strong> {recommendations.source.replace('_', ' ')}
              </p>
              <p className="text-xs text-lime-600 mt-1">
                Found {recommendations.recommendations.length} university recommendations
              </p>
            </div>

            {/* Accommodations Needed */}
            {recommendations.needed_accommodations && recommendations.needed_accommodations.length > 0 && (
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h3 className="font-semibold text-blue-900 mb-2">Recommended Accommodations:</h3>
                <ul className="text-sm text-blue-800">
                  {recommendations.needed_accommodations.slice(0, 4).map((accommodation: string, index: number) => (
                    <li key={index} className="flex items-center mb-1">
                      <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                      {accommodation}
                    </li>
                  ))}
                  {recommendations.needed_accommodations.length > 4 && (
                    <li className="text-blue-600 text-xs">
                      +{recommendations.needed_accommodations.length - 4} more...
                    </li>
                  )}
                </ul>
              </div>
            )}
  

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
          {/* Roadmap SVG */}
          <div className="relative w-full h-full flex items-center justify-center">
            {svg ? (
              <div
                className="absolute bottom-0 right-0 max-h-full max-w-full object-contain z-0 pointer-events-none select-none"
                dangerouslySetInnerHTML={{ __html: svg }}
              />
            ) : (
              <p>Loading roadmap...</p>
            )}
          </div>
        </div>
      </main>
      {/* Navigation Buttons */}
      <div className="absolute bottom-8 left-8 flex flex-col gap-4 z-20">
        <button
          onClick={() => navigate("/eligibility")}
          className="bg-[#92BD3A] text-white px-5 py-2 rounded-md hover:bg-lime-600 transition"
        >
          Eligibility & Prerequisites
        </button>
        <button
          onClick={() => navigate("/required")}
          className="bg-[#92BD3A] text-white px-5 py-2 rounded-md hover:bg-lime-600 transition"
        >
          Required Documents
        </button>
        <button
          onClick={() => navigate("/submission")}
          className="bg-[#92BD3A] text-white px-5 py-2 rounded-md hover:bg-lime-600 transition"
        >
          Application Submission
        </button>
      </div>
    </div>
  );
}
