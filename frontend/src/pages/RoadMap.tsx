import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import type { RecommendationResponse, StudentProfile } from "../services/api";
import roadBgSvg from "../assets/road_bg.svg";


interface RoadmapData {
  studentProfile: StudentProfile;
  recommendations: RecommendationResponse;
}


export default function RoadMap() {
  const navigate = useNavigate();
  const [roadmapData, setRoadmapData] = useState<RoadmapData | null>(null);
  const [loading, setLoading] = useState(true);
  const [university, setUniversity] = useState<string>("Your University");

  useEffect(() => {
    // Load roadmap data from session storage
    function loadRoadmapData() {
      // First, try to get actual data from sessionStorage (set by UserInput/Recommendations)
      const storedRecommendations = sessionStorage.getItem('recommendations');
      const storedProfile = sessionStorage.getItem('studentProfile');
      
      let roadmapDataToUse: RoadmapData | null = null;

      if (storedRecommendations && storedProfile) {
        try {
          // Combine the actual recommendations and profile
          const recommendations = JSON.parse(storedRecommendations);
          const studentProfile = JSON.parse(storedProfile);
          roadmapDataToUse = {
            studentProfile,
            recommendations
          };
        } catch (error) {
          console.error('Error parsing stored recommendations/profile:', error);
        }
      }

      // If no actual data, check for legacy roadmapData or use dummy data
      if (!roadmapDataToUse) {
        const storedRoadmapData = sessionStorage.getItem('roadmapData');
        if (storedRoadmapData) {
          try {
            roadmapDataToUse = JSON.parse(storedRoadmapData);
          } catch (error) {
            console.error('Error parsing stored roadmapData:', error);
          }
        }
      }

      // Last resort: create dummy data for testing
      if (!roadmapDataToUse) {
        roadmapDataToUse = {
          studentProfile: {
            mental_health: "None",
            physical_health: "None",
            courses: "General",
            gpa: 3.0,
            severity: "moderate" as const
          },
          recommendations: {
            success: true,
            source: "gemini",
            recommendations: [
              { 
                name: "Graduation Book University",
                score: 4.5,
                accessibility_rating: 4.5,
                disability_support_rating: 4.8,
                available_accommodations: ["Graduation Book", "Wheelchair Access"],
                location: "Ontario",
                reason: "Excellent disability support services"
              }
            ],
            needed_accommodations: ["Graduation Book", "Wheelchair Access", "Extra Time", "Quiet Room"]
          }
        };
      }

      setRoadmapData(roadmapDataToUse);
      const universityName = roadmapDataToUse.recommendations?.recommendations?.[0]?.name || "Your University";
      setUniversity(universityName);
      
      setLoading(false);
    }
    loadRoadmapData();
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
              Your step‑by‑step plan for {university}
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
                      {accommodation === "Graduation Book" && (
                        <span className="ml-2 px-2 py-1 bg-yellow-200 text-yellow-900 rounded text-xs font-semibold">Special</span>
                      )}
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
          {/* Roadmap SVG with Checkpoints */}
          <div className="relative w-full h-full flex items-center justify-center">
            <img 
              src={roadBgSvg} 
              alt="Roadmap background" 
              className="w-full h-auto max-w-full object-contain"
            />
            
            {/* Checkpoint 1: Eligibility and Prerequisites */}
            <div 
              className="absolute top-[15%] right-[10%] flex flex-col items-center cursor-pointer group"
              onClick={() => navigate('/eligibility')}
            >
              <div className="w-16 h-16 border-4 border-dashed border-[#92BD3A] rounded-full group-hover:border-lime-600 transition-colors"></div>
              <p className="mt-2 text-sm font-medium text-gray-800 group-hover:text-lime-600 transition-colors">
                Eligibility and Prerequisites
              </p>
            </div>

            {/* Checkpoint 2: Required Documents */}
            <div 
              className="absolute top-[40%] left-[5%] flex flex-col items-center cursor-pointer group"
              onClick={() => navigate('/required')}
            >
              <div className="w-16 h-16 border-4 border-dashed border-[#92BD3A] rounded-full group-hover:border-lime-600 transition-colors"></div>
              <p className="mt-2 text-sm font-medium text-gray-800 group-hover:text-lime-600 transition-colors">
                Required Documents
              </p>
            </div>

            {/* Checkpoint 3: Financial Aid */}
            <div 
              className="absolute top-[65%] right-[15%] flex flex-col items-center cursor-pointer group"
              onClick={() => navigate('/submission')}
            >
              <div className="w-16 h-16 border-4 border-dashed border-[#92BD3A] rounded-full group-hover:border-lime-600 transition-colors"></div>
              <p className="mt-2 text-sm font-medium text-white-800 group-hover:text-lime-600 transition-colors">
                Financial Aid
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
