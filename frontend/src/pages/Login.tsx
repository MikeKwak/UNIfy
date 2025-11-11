import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import NavBar from "../components/NavBar";
import { useAuth } from "../contexts/AuthContext";
import type { FormEvent } from "react";
import logoSvg from "../assets/logo.svg";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { signIn, resetPassword, confirmResetPassword } = useAuth();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    verificationCode: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [resetPasswordSent, setResetPasswordSent] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const storeAuthToken = async (email: string, password: string) => {
    const encoder = new TextEncoder();
    const data = encoder.encode(email + password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    localStorage.setItem("authToken", hashHex);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (resetPasswordSent) {
        await confirmResetPassword(formData.email, formData.verificationCode, formData.password);
        setResetPasswordSent(false);
        const from = location.state?.from?.pathname || "/login";
        navigate(from, { replace: true });
      } else {
        await signIn(formData.email, formData.password);
        // Redirect to the page they were trying to access, or default to information
        const from = location.state?.from?.pathname || "/information";
        navigate(from, { replace: true });
      }
    } catch (error: any) {
      console.error(resetPasswordSent ? "Reset password error:" : "Login error:", error);
      setError(error.message || (resetPasswordSent ? "An error occurred during password reset" : "An error occurred during login"));
    } finally {
      setLoading(false);
      await storeAuthToken(formData.email, formData.password);
    }
  };

  const handleResetPassword = async () => {
    // Implement password reset logic or navigation here
    try {
      await resetPassword(formData.email);
    } catch (error: any) {
      console.error("Reset password error:", error);
      setError(error.message || "An error occurred during password reset");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-gray-100 flex items-center justify-center min-h-screen">
      {/* Navbar */}
      <NavBar />

      {/* Login Card */}
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md mt-20">
        {/* Logo + Header */}
        <div className="flex flex-col items-center mb-8">
          <img src={logoSvg} alt="UNIfy logo" className="w-12 h-12 mb-2" />
          <h1 className="text-2xl font-bold">UNIfy</h1>
          <p className="text-gray-600 mt-2">Log in to your account</p>
        </div>

        {/* Login Form */}
        <form className="space-y-6" onSubmit={handleSubmit}>
          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
              {error}
            </div>
          )}

          {resetPasswordSent && (
            <div className="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-md">
              A password reset confirmation email has been sent.
            </div>
          )}

          {/* Email */}
          <div>
            <label
              htmlFor="email"
              className="block  font-medium text-gray-700"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
            />
          </div>

          {/* Password */}
            {
            resetPasswordSent ? (
              <div>
              <label
                htmlFor="verificationCode"
                className="block  font-medium text-gray-700"
              >
                Verification Code
              </label>
              <input
                type="text"
                id="verificationCode"
                name="verificationCode"
                required
                value={formData.verificationCode}
                onChange={handleChange}
                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
              />
              </div>
            ) : null}
            <div>
              <label
              htmlFor="password"
              className="block  font-medium text-gray-700"
              >
              {resetPasswordSent ? "New Password" : "Password"}
              </label>
              <input
                type="password"
                id="password"
                name="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-lime-500 focus:border-lime-500"
              />
            </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-lime-500 hover:bg-lime-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-md transition"
          >
            {loading ? "Signing In..." : resetPasswordSent ? "Reset Password" : "Log In"}
          </button>

          {
            resetPasswordSent ? null : (
              <div className="text-center mt-4">
                <button
                  type="button"
                  onClick={() => {
                  handleResetPassword();
                  setResetPasswordSent(true);
                  }}
                  className="text-lime-600 hover:underline  bg-transparent border-none cursor-pointer"
                >
                  Forgot password?
                </button>
              </div>
            )}
        </form>
      </div>
    </div>
  );
}
