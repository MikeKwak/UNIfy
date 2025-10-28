import { useNavigate } from "react-router-dom";

type PageHeaderProps = {
  title: string;
  description: string;
};

export default function PageHeader({ title, description }: PageHeaderProps) {
  const navigate = useNavigate();

  return (
    <div className="mb-10">
      {/* Back button */}
      <button
        onClick={() => navigate(-1)}
        className="bg-lime-600 text-white px-5 py-2 rounded-md hover:bg-lime-700 transition"
      >
        Back to Roadmap
      </button>

      {/* Title */}
      <h1 className="text-3xl sm:text-4xl md:text-5xl font-semibold mt-8">
        {title}
      </h1>
      <p className="text-gray-600 mt-2 mb-6">{description}</p>

      <hr className="border-gray-300" />
    </div>
  );
}
