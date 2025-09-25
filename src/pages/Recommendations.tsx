import NavBar from "../components/NavBar";
import PageHeader from "../components/PageHeader";

export default function Recommendations() {
  return (
    <div className="font-blmelody bg-white text-gray-900 min-h-screen">
      {/* Navbar */}
      <NavBar />

      {/* Body */}
      <main className="pt-32 pb-16 px-4 max-w-5xl mx-auto">
        <PageHeader
          title="University Recommendations"
          description="Review alternative programs and institutions aligned with your academic and accessibility profile."
        />

        {/* Recommendations Box */}
        <div className="border border-lime-400 rounded-md p-8 min-h-[250px] flex items-center justify-center text-gray-400">
          {/* Recommendations will go here */}
        </div>
      </main>
    </div>
  );
}
