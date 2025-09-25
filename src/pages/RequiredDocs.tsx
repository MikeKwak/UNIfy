import NavBar from "../components/NavBar";
import PageHeader from "../components/PageHeader";

export default function RequiredDocs() {
  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />

      {/* Body */}
      <main className="pt-32 pb-16 px-4 max-w-6xl mx-auto">
        <PageHeader
          title="Required Documents"
          description="Let’s make sure you have the right documents to access accommodations at each school."
        />

        {/* Requirements Section */}
        <div className="grid grid-cols-2 gap-12">
          {/* Required Documents */}
          <div className="flex items-start space-x-3">
            <label className="whitespace-nowrap mt-2">
              Required Documents:
            </label>
            <textarea
              rows={6}
              className="border border-lime-400 rounded-md px-3 py-2 w-full"
            />
          </div>

          {/* Step-by-step Guide */}
          <div className="flex items-start space-x-3">
            <label className="whitespace-nowrap mt-2">
              Step-by-step guide:
            </label>
            <textarea
              rows={6}
              className="border border-lime-400 rounded-md px-3 py-2 w-full"
            />
          </div>
        </div>
      </main>
    </div>
  );
}
