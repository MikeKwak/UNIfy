import { useState } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "../components/NavBar";
import { useAuth } from "../contexts/AuthContext";

export default function Signup() {
    const navigate = useNavigate();
    const { signUp, confirmSignUp } = useAuth();
    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        confirmPassword: ""
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [confirmationCode, setConfirmationCode] = useState("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        
        if (form.password !== form.confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        if (form.password.length < 8) {
            setError("Password must be at least 8 characters long");
            return;
        }

        setLoading(true);

        try {
            await signUp(form.email, form.password, form.name);
            setShowConfirmation(true);
        } catch (error: any) {
            console.error("Signup error:", error);
            setError(error.message || "An error occurred during signup");
        } finally {
            setLoading(false);
        }
    };

    const handleConfirmation = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            await confirmSignUp(form.email, confirmationCode);
            navigate("/login");
        } catch (error: any) {
            console.error("Confirmation error:", error);
            setError(error.message || "An error occurred during confirmation");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-gray-100 flex items-center justify-center min-h-screen">
            <NavBar />
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md mt-20">
                <div className="flex flex-col items-center mb-8">
                    <img src="/logo.svg" alt="UNIfy logo" className="w-12 h-12 mb-2" />
                    <h1 className="text-2xl font-bold">
                        {showConfirmation ? "Confirm Your Account" : "Sign Up"}
                    </h1>
                    <p className="text-gray-600 mt-2">
                        {showConfirmation 
                            ? "Enter the confirmation code sent to your email" 
                            : "Create your UNIfy account"
                        }
                    </p>
                </div>
                
                {showConfirmation ? (
                    <form className="space-y-6" onSubmit={handleConfirmation}>
                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
                                {error}
                            </div>
                        )}
                        
                        <div>
                            <label htmlFor="confirmationCode" className="block text-sm font-medium text-gray-700">
                                Confirmation Code
                            </label>
                            <input
                                type="text"
                                id="confirmationCode"
                                name="confirmationCode"
                                required
                                value={confirmationCode}
                                onChange={(e) => setConfirmationCode(e.target.value)}
                                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
                                placeholder="Enter 6-digit code"
                            />
                        </div>
                        
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-lime-500 hover:bg-lime-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-md transition"
                        >
                            {loading ? "Confirming..." : "Confirm Account"}
                        </button>
                        
                        <div className="text-center">
                            <button
                                type="button"
                                onClick={() => setShowConfirmation(false)}
                                className="text-sm text-lime-600 hover:underline"
                            >
                                Back to Sign Up
                            </button>
                        </div>
                    </form>
                ) : (
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
                                {error}
                            </div>
                        )}
                        
                        <div>
                            <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                required
                                value={form.name}
                                onChange={handleChange}
                                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
                            />
                        </div>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                required
                                value={form.email}
                                onChange={handleChange}
                                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                required
                                value={form.password}
                                onChange={handleChange}
                                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
                            />
                            <p className="text-xs text-gray-500 mt-1">Password must be at least 8 characters long</p>
                        </div>
                        <div>
                            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">Confirm Password</label>
                            <input
                                type="password"
                                id="confirmPassword"
                                name="confirmPassword"
                                required
                                value={form.confirmPassword}
                                onChange={handleChange}
                                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-lime-500 hover:bg-lime-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-md transition"
                        >
                            {loading ? "Creating Account..." : "Sign Up"}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
}
