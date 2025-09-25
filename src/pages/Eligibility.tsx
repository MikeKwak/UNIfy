import NavBar from "../components/NavBar";
import PageHeader from "../components/PageHeader";

export default function Eligibility() {
  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />

      {/* Body */}
      <main className="pt-32 pb-16 px-4 max-w-6xl mx-auto">
        <PageHeader
          title="Eligibility and Prerequisites"
          description="Let’s see if you meet the minimum requirements for your target programs."
        />

        {/* Requirements Display */}
        <div className="space-y-12">
          {/* GPA */}
          <div className="grid grid-cols-12 gap-4 items-start">
            <label className="col-span-2">Your GPA:</label>
            <input
              type="text"
              className="col-span-2 border border-lime-400 rounded-md px-3 py-2"
            />

            <label className="col-span-2">Required GPA:</label>
            <input
              type="text"
              className="col-span-2 border border-lime-400 rounded-md px-3 py-2"
            />

            <div className="col-span-4 flex items-start space-x-3">
              <img
                src="/src/assets/arrowRight.svg"
                alt="Arrow"
                className="h-6 w-20"
              />
              <span className="font-medium">Meets Requirement</span>
            </div>
          </div>

          {/* Courses */}
          <div className="grid grid-cols-12 gap-4 items-start">
            <label className="col-span-2">Your Completed Courses:</label>
            <textarea
              rows={3}
              className="col-span-2 border border-lime-400 rounded-md px-3 py-2"
            />

            <label className="col-span-2">Required Courses:</label>
            <textarea
              rows={3}
              className="col-span-2 border border-lime-400 rounded-md px-3 py-2"
            />

            <div className="col-span-4 flex items-start space-x-3">
              <img
                src="/src/assets/arrowRight.svg"
                alt="Arrow"
                className="h-6 w-20"
              />
              <span className="font-medium">Missing:</span>
            </div>
          </div>

          {/* Disabilities */}
          <div className="grid grid-cols-12 gap-4 items-start">
            <label className="col-span-2">Your Disabilities:</label>
            <textarea
              rows={3}
              className="col-span-2 border border-lime-400 rounded-md px-3 py-2"
            />

            <label className="col-span-2">Accommodations:</label>
            <textarea
              rows={3}
              className="col-span-2 border border-lime-400 rounded-md px-3 py-2"
            />

            <div className="col-span-4 flex items-start space-x-3">
              <img
                src="/src/assets/arrowRight.svg"
                alt="Arrow"
                className="h-6 w-20"
              />
              <span className="font-medium">Good Fit</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
