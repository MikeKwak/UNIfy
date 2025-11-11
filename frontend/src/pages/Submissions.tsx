import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import PageHeader from "../components/PageHeader";
import type { StudentProfile, RecommendationResponse } from "../services/api";

export default function Submission() {
  const navigate = useNavigate();
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [checklist, setChecklist] = useState({
    application: false,
    transcripts: false,
    essays: false,
    recommendations: false,
    disabilityServices: false,
    medicalDocs: false,
    osap: false,
    scholarships: false,
  });

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

  // Check if all items are checked
  const allChecked = Object.values(checklist).every(value => value === true);
  
  // Get university name
  const universityName = recommendations?.recommendations?.[0]?.name || "your chosen university";

  const handleCheckboxChange = (key: keyof typeof checklist) => {
    setChecklist(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />
      {/* Body */}
      <main className="pt-32 pb-16 px-4 max-w-6xl mx-auto">
        <PageHeader
          title="Financial Aid & Application Submission"
          description="Let's get your applications and accommodations submitted on time."
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

            {/* Financial Aid Section */}
            <div className="mb-12">
              <h2 className="text-2xl font-semibold mb-6 text-lime-800">Financial Aid Options</h2>
              
              <div className="space-y-6">
                {/* OSAP */}
                <div className="border border-lime-400 rounded-md p-6 bg-white">
                  <h3 className="text-xl font-semibold mb-3 text-lime-700">Ontario Student Assistance Program (OSAP)</h3>
                  <p className="text-gray-700 mb-3">
                    OSAP provides grants and loans to help Ontario students pay for college or university. Students with disabilities may be eligible for additional funding.
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-2 mb-4">
                    <li>Bursary for Students with Disabilities (BSWD): Up to $2,000/term</li>
                    <li>Canada Student Grant for Students with Disabilities: Up to $2,000/year</li>
                    <li>Equipment and Services Bursary: Up to $20,000/year for disability-related equipment</li>
                  </ul>
                  <a 
                    href="https://www.ontario.ca/page/osap-ontario-student-assistance-program" 
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-lime-600 hover:text-lime-700 underline"
                  >
                    Apply for OSAP →
                  </a>
                </div>

                {/* University-Specific Aid */}
                <div className="border border-lime-400 rounded-md p-6 bg-white">
                  <h3 className="text-xl font-semibold mb-3 text-lime-700">University Scholarships & Bursaries</h3>
                  <p className="text-gray-700 mb-3">
                    Most universities offer entrance scholarships, in-course scholarships, and accessibility-focused bursaries.
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-2">
                    <li>Entrance scholarships: Based on admission average (typically 80%+)</li>
                    <li>Accessibility scholarships: For students with documented disabilities</li>
                    <li>Need-based bursaries: Based on financial need</li>
                    <li>Faculty-specific awards: Check with your specific program</li>
                  </ul>
                </div>

                {/* External Scholarships */}
                <div className="border border-lime-400 rounded-md p-6 bg-white">
                  <h3 className="text-xl font-semibold mb-3 text-lime-700">External Scholarships</h3>
                  <p className="text-gray-700 mb-3">
                    Many organizations offer scholarships for students with disabilities.
                  </p>
                  <ul className="list-disc list-inside text-gray-700 space-y-2">
                    <li>Google Lime Scholarship: For students with disabilities in computer science</li>
                    <li>TD Scholarships for Community Leadership</li>
                    <li>RBC Foundation Scholarships</li>
                    <li>Local community organizations and foundations</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Application Submission Timeline */}
            <div className="mb-12">
              <h2 className="text-2xl font-semibold mb-6 text-lime-800">Application Submission Timeline</h2>
              
              <div className="border border-lime-400 rounded-md p-6 bg-lime-50">
                <div className="space-y-4">
                  <div className="flex items-start space-x-4">
                    <div className="bg-lime-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">1</div>
                    <div>
                      <h4 className="font-semibold text-lime-800">October - November: Early Applications</h4>
                      <p className="text-gray-700">Submit applications for early admission programs. Some universities offer advantages for early applicants.</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="bg-lime-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">2</div>
                    <div>
                      <h4 className="font-semibold text-lime-800">January: Regular Applications Deadline</h4>
                      <p className="text-gray-700">Most Ontario universities have deadlines in mid-to-late January for September admission.</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="bg-lime-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">3</div>
                    <div>
                      <h4 className="font-semibold text-lime-800">February - March: Disability Services Registration</h4>
                      <p className="text-gray-700">Register with university disability services and submit accommodation documentation (can be done after admission).</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="bg-lime-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">4</div>
                    <div>
                      <h4 className="font-semibold text-lime-800">April - May: Scholarship Applications</h4>
                      <p className="text-gray-700">Apply for university and external scholarships. Many have spring deadlines.</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="bg-lime-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">5</div>
                    <div>
                      <h4 className="font-semibold text-lime-800">June: Accept Offers & Apply for OSAP</h4>
                      <p className="text-gray-700">Accept your university offer and submit OSAP application (opens in June for fall term).</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="bg-lime-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">6</div>
                    <div>
                      <h4 className="font-semibold text-lime-800">July - August: Finalize Accommodations</h4>
                      <p className="text-gray-700">Confirm your accommodations are in place before classes start in September.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Checklist */}
            <div className="border border-lime-400 rounded-md p-6 bg-blue-50">
              <h3 className="text-xl font-semibold mb-4 text-blue-900">Submission Checklist</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.application}
                      onChange={() => handleCheckboxChange('application')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('application')}>
                      University application submitted
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.transcripts}
                      onChange={() => handleCheckboxChange('transcripts')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('transcripts')}>
                      Transcripts sent
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.essays}
                      onChange={() => handleCheckboxChange('essays')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('essays')}>
                      Supplementary essays completed
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.recommendations}
                      onChange={() => handleCheckboxChange('recommendations')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('recommendations')}>
                      Letters of recommendation requested
                    </label>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.disabilityServices}
                      onChange={() => handleCheckboxChange('disabilityServices')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('disabilityServices')}>
                      Disability services registration
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.medicalDocs}
                      onChange={() => handleCheckboxChange('medicalDocs')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('medicalDocs')}>
                      Medical documentation submitted
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.osap}
                      onChange={() => handleCheckboxChange('osap')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('osap')}>
                      OSAP application submitted
                    </label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      className="w-5 h-5 cursor-pointer" 
                      checked={checklist.scholarships}
                      onChange={() => handleCheckboxChange('scholarships')}
                    />
                    <label className="text-gray-700 cursor-pointer" onClick={() => handleCheckboxChange('scholarships')}>
                      Scholarship applications completed
                    </label>
                  </div>
                </div>
              </div>

              {/* Congratulations Message */}
              {allChecked && (
                <div className="mt-6 p-6 bg-lime-500 text-white rounded-lg text-center animate-pulse">
                  <h4 className="text-2xl font-bold mb-2"> Congratulations! </h4>
                  <p className="text-lg">
                    You've completed the submission checklist! You're gonna crush it at {universityName}!
                  </p>
                </div>
              )}
            </div>
          </>
        )}
      </main>
    </div>
  );
}
