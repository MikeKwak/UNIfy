import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import PageHeader from "../components/PageHeader";
import type { StudentProfile, RecommendationResponse } from "../services/api";

export default function Eligibility() {
  const navigate = useNavigate();
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);

  useEffect(() => {
    // Load data from sessionStorage
    const storedProfile = sessionStorage.getItem('studentProfile');
    const storedRecommendations = sessionStorage.getItem('recommendations');

    if (storedProfile) {
      try {
        setStudentProfile(JSON.parse(storedProfile));
      } catch (error) {
        console.error('Error parsing student profile:', error);
      }
    }

    if (storedRecommendations) {
      try {
        setRecommendations(JSON.parse(storedRecommendations));
      } catch (error) {
        console.error('Error parsing recommendations:', error);
      }
    }
  }, []);

  // Calculate if GPA meets requirement (3.0 is common threshold)
  const requiredGPA = 3.0;
  const meetsGPARequirement = studentProfile ? studentProfile.gpa >= requiredGPA : false;

  // Get accommodations from recommendations
  const accommodations = recommendations?.needed_accommodations || [];

  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />

      {/* Body */}
      <main className="pt-32 pb-16 px-4 max-w-6xl mx-auto">
        <PageHeader
          title="Eligibility and Prerequisites"
          description="Let's see if you meet the minimum requirements for your target programs."
        />

        {!studentProfile ? (
          <div className="text-center py-8">
            <p className="text-gray-600 mb-4">No profile data found. Please complete the user input form first.</p>
            <button
              onClick={() => navigate('/information')}
              className="bg-lime-500 hover:bg-lime-600 text-white px-6 py-2 rounded-md"
            >
              Go to User Input
            </button>
          </div>
        ) : (
          <>
            {/* Requirements Display */}
            <div className="space-y-12">
              {/* GPA */}
              <div className="grid grid-cols-12 gap-4 items-start">
                <label className="col-span-2">Your GPA:</label>
                <input
                  type="text"
                  value={studentProfile.gpa}
                  readOnly
                  className="col-span-2 border border-lime-400 rounded-md px-3 py-2 bg-lime-50"
                />

                <label className="col-span-2">Required GPA:</label>
                <input
                  type="text"
                  value={requiredGPA}
                  readOnly
                  className="col-span-2 border border-lime-400 rounded-md px-3 py-2 bg-gray-50"
                />

                <div className="col-span-4 flex items-start space-x-3">
                  <img
                    src="/src/assets/arrowRight.svg"
                    alt="Arrow"
                    className="h-6 w-20"
                  />
                  <span className={`font-medium ${meetsGPARequirement ? 'text-green-600' : 'text-red-600'}`}>
                    {meetsGPARequirement ? '✓ Meets Requirement' : '✗ Below Requirement'}
                  </span>
                </div>
              </div>

              {/* Courses */}
              <div className="grid grid-cols-12 gap-4 items-start">
                <label className="col-span-2">Your Program:</label>
                <textarea
                  rows={3}
                  value={studentProfile.courses}
                  readOnly
                  className="col-span-2 border border-lime-400 rounded-md px-3 py-2 bg-lime-50"
                />

                <label className="col-span-2">Program Requirements:</label>
                <textarea
                  rows={3}
                  value="Typical requirements:\n- High School Diploma\n- Prerequisites for major\n- English proficiency"
                  readOnly
                  className="col-span-2 border border-lime-400 rounded-md px-3 py-2 bg-gray-50"
                />

                <div className="col-span-4 flex items-start space-x-3">
                  <img
                    src="/src/assets/arrowRight.svg"
                    alt="Arrow"
                    className="h-6 w-20"
                  />
                  <span className="font-medium text-green-600">✓ On Track</span>
                </div>
              </div>

              {/* Disabilities & Accommodations */}
              <div className="grid grid-cols-12 gap-4 items-start">
                <label className="col-span-2">Your Health Profile:</label>
                <textarea
                  rows={3}
                  value={`Mental Health: ${studentProfile.mental_health}\nPhysical Health: ${studentProfile.physical_health}\nSeverity: ${studentProfile.severity}`}
                  readOnly
                  className="col-span-2 border border-lime-400 rounded-md px-3 py-2 bg-lime-50"
                />

                <label className="col-span-2">Available Accommodations:</label>
                <textarea
                  rows={3}
                  value={accommodations.length > 0 ? accommodations.join('\n') : 'Loading accommodations...'}
                  readOnly
                  className="col-span-2 border border-lime-400 rounded-md px-3 py-2 bg-gray-50"
                />

                <div className="col-span-4 flex items-start space-x-3">
                  <img
                    src="/src/assets/arrowRight.svg"
                    alt="Arrow"
                    className="h-6 w-20"
                  />
                  <span className="font-medium text-green-600">✓ Good Fit</span>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
