import { type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { useState } from "react"; 
import { generateRoadmapRecommendations, type StudentProfile } from "../services/api";


export default function UserInput() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);


  //function handleSubmit(e: FormEvent<HTMLFormElement>) {
  //  e.preventDefault();
  //  // Add validation later

  //  navigate("/roadmap");
  //}

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);
  
    try {
      const formData = new FormData(e.currentTarget);
      
      const studentProfile: StudentProfile = {
        mental_health: formData.get('disability') as string || 'None',
        physical_health: formData.get('disability-type') === 'Physical' ? 'Mobility' : 'None',
        courses: formData.get('program') as string || 'General Studies',
        gpa: parseFloat(formData.get('gpa') as string) || 3.0,
        severity: 'moderate'
      };
  
      // Step 1: DB verification, Step 2: LLM verification
      const recommendations = await generateRoadmapRecommendations(studentProfile);
      
      sessionStorage.setItem('roadmapData', JSON.stringify({
        studentProfile,
        recommendations
      }));

      navigate("/roadmap");
    
  } catch (err) {
    setError('Failed to generate roadmap. Please try again.');
  } finally {
    setLoading(false);
  }
}



  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />

      {/* Form Section */}
      <section className="pt-32 pb-16 px-4 max-w-3xl mx-auto">
        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800">{error}</p>
          </div>
        )}
        <h2 className="text-3xl mb-2">Let’s personalize your journey.</h2>
        <p className="mb-8 text-gray-600">
          Tell us a bit about your academic background and accessibility needs
          so we can build your custom university admissions roadmap.
        </p>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="space-y-6 bg-white p-8 rounded shadow"
        >
          {/* Full Name */}
          <div>
            <label
              htmlFor="name"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              Full Name
            </label>
            <input
              id="name"
              name="name"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            />
          </div>

          {/* Email */}
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            />
          </div>

          {/* High School */}
          <div>
            <label
              htmlFor="school"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              High School
            </label>
            <input
              id="school"
              name="school"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            />
          </div>

          {/* GPA */}
          <div>
            <label
              htmlFor="gpa"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              Current GPA
            </label>
            <input
              id="gpa"
              name="gpa"
              type="number"
              step="0.1"
              max={4.0}
              min={0.0}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            />
          </div>

          {/* Completed High School Courses */}
          <div>
            <label
              htmlFor="courses"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              Completed High School Courses
            </label>
            <div className="space-y-3">
              <select
                id="courses"
                name="courses"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
              >
                <option value="">Select a course</option>
                <option value="Biology">Biology</option>
                <option value="Calculus">Calculus</option>
                <option value="English">English</option>
                <option value="Physics">Physics</option>
              </select>

              <button type="button" className="text-sm hover:underline">
                + Add more
              </button>
            </div>
          </div>

          {/* University & Program Preference + Add more */}
          <div>
            <label className="block text-sm font-medium mb-2 text-lime-600">
              University & Program Preference
            </label>
            <select
              id="preference"
              name="preference"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            >
              <option value="">Select a program</option>
            </select>
          </div>

          {/* Application Round */}
          <fieldset>
            <legend className="block text-sm font-medium mb-1 text-lime-600">
              Application Round (Early/General Round)
            </legend>
            <div className="flex flex-wrap gap-6">
              <label className="inline-flex items-center gap-2">
                <input type="radio" name="app-round" value="Early" />
                Early
              </label>
              <label className="inline-flex items-center gap-2">
                <input type="radio" name="app-round" value="General" /> General
              </label>
            </div>
          </fieldset>

          {/* Financial Preference */}
          <div>
            <label
              htmlFor="financial-preference"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              Financial Preference
            </label>
            <select
              id="financial-preference"
              name="financial-preference"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            >
              <option value="">Select an option</option>
            </select>
          </div>

          {/* Extracurriculars */}
          <div>
            <label
              htmlFor="ecs"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              List of Extracurriculars (Optional)
            </label>
            <textarea
              id="ecs"
              name="ecs"
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            />
          </div>

          {/* Disability Type */}
          <fieldset>
            <legend className="block text-sm font-medium mb-1 text-lime-600">
              Disability Type
            </legend>
            <div className="flex flex-wrap gap-6">
              <label className="inline-flex items-center gap-2">
                <input type="radio" name="disability-type" value="Mental" />
                Mental
              </label>
              <label className="inline-flex items-center gap-2">
                <input type="radio" name="disability-type" value="Physical" />
                Physical
              </label>
              <label className="inline-flex items-center gap-2">
                <input type="radio" name="disability-type" value="Both" />
                Both
              </label>
            </div>
          </fieldset>

          {/* Disability */}
          <div>
            <label
              htmlFor="disability"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              Disability
            </label>
            <select
              id="disability"
              name="disability"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            >
              <option value="">Select an option</option>
            </select>
          </div>

          {/* Program Interests */}
          <div>
            <label
              htmlFor="program"
              className="block text-sm font-medium mb-1 text-lime-600"
            >
              Program Interests
            </label>
            <input
              id="program"
              name="program"
              placeholder="e.g., Engineering, Psychology"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-lime-500 focus:border-lime-500"
            />
          </div>

          


          <button
            type="submit"
            disabled={loading}
            className="w-full bg-lime-500 hover:bg-lime-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-2 px-4 rounded-md transition"
          >
            {loading ? 'Generating Roadmap...' : 'Generate Roadmap'}
          </button>
        </form>
      </section>
    </div>
  );
}
