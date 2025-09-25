import NavBar from "../components/NavBar";
import PageHeader from "../components/PageHeader";

export default function Submission() {

  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />
      {/* Body */}
      <main className="pt-32 pb-16 px-4 max-w-6xl mx-auto">
        <PageHeader
          title="Application Submission Steps"
          description="Let’s get your applications and accommodations submitted on time."
        />
        {/* Content placeholder */}
        <div className="border border-lime-400 rounded-md p-8 min-h-[250px] flex items-center justify-center text-gray-400">
        </div>
      </main>
    </div>
  );
}
