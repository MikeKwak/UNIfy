import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import PageHeader from "../components/PageHeader";
import type { StudentProfile, RecommendationResponse } from "../services/api";

export default function RequiredDocs() {
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

  // Build required documents list
  const requiredDocs = `General Application Documents:
• High school transcripts or university transcripts
• Personal statement or essay
• Letters of recommendation (2-3)
• Application form (completed online)
• Application fee payment confirmation
• Government-issued ID

Accommodation-Specific Documents:
• Medical documentation or diagnosis letter
• Psychoeducational assessment (if applicable)
• Doctor's letter outlining required accommodations
• Previous accommodation plans (if any)
• Functional impact statement`;

  // Build step-by-step guide
  const stepByStepGuide = `Step 1: Gather General Documents
Collect transcripts, write personal statement, and request recommendation letters.

Step 2: Obtain Medical Documentation
Visit your healthcare provider to get official documentation of your condition.

Step 3: Complete Application Forms
Fill out the main application and disability services registration forms.

Step 4: Submit to Disability Services
Submit accommodation documents to the university's disability services office (separate from admissions).

Step 5: Follow Up
Contact disability services 2-3 weeks after submission to confirm receipt and discuss next steps.

Step 6: Schedule Assessment
If required, schedule any additional assessments or meetings with the disability services team.`;

  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />

      {/* Body */}
      <main className="pt-32 pb-16 px-4 max-w-6xl mx-auto">
        <PageHeader
          title="Required Documents"
          description="Let's make sure you have the right documents to access accommodations at each school."
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
            {/* Profile Summary */}
            <div className="mb-8 p-4 bg-lime-50 border border-lime-200 rounded-md">
              <p className=" text-lime-800">
                <strong>Your Profile:</strong> {studentProfile.courses} | GPA: {studentProfile.gpa} | 
                Mental Health: {studentProfile.mental_health} | Physical Health: {studentProfile.physical_health}
              </p>
            </div>

            {/* Requirements Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
              {/* Required Documents */}
              <div className="flex flex-col space-y-3">
                <label className="font-semibold text-lg">
                  Required Documents:
                </label>
                <textarea
                  rows={18}
                  value={requiredDocs}
                  readOnly
                  className="border border-lime-400 rounded-md px-3 py-2 w-full bg-lime-50"
                />
              </div>

              {/* Step-by-step Guide */}
              <div className="flex flex-col space-y-3">
                <label className="font-semibold text-lg">
                  Step-by-step Guide:
                </label>
                <textarea
                  rows={18}
                  value={stepByStepGuide}
                  readOnly
                  className="border border-lime-400 rounded-md px-3 py-2 w-full bg-gray-50"
                />
              </div>
            </div>

            {/* Recommended Accommodations */}
            {recommendations?.needed_accommodations && recommendations.needed_accommodations.length > 0 && (
              <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-md">
                <h3 className="font-semibold text-blue-900 mb-3">Your Recommended Accommodations:</h3>
                <div className="flex flex-wrap gap-2">
                  {recommendations.needed_accommodations.map((accommodation, index) => (
                    <span
                      key={index}
                      className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                    >
                      {accommodation}
                    </span>
                  ))}
                </div>
                <p className="mt-3  text-blue-700">
                  Make sure to include documentation that supports your need for these specific accommodations.
                </p>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
