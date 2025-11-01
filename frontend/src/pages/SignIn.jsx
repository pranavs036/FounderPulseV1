import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "@/auth/AuthContext";

export default function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { signIn, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/dashboard";

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await signIn(email.trim(), password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message || "Unable to sign in");
    }
  };

  useEffect(() => {
    if (user) {
      navigate("/dashboard", { replace: true });
    }
  }, [user, navigate]);

  return (
    <div className="min-h-dvh grid place-items-center bg-[#0D1117] px-6">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-md rounded-2xl border border-[#6366F1]/20 bg-[#11131A]/50 backdrop-blur-sm p-8 shadow-2xl"
      >
        <h1 className="text-2xl font-semibold tracking-tight text-white">Welcome back</h1>
        <form className="mt-6 space-y-4" onSubmit={onSubmit}>
          <div>
            <label className="block text-sm mb-1 text-[#F3F4F6]/80">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-[#6366F1]/30 bg-[#0D1117]/50 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6366F1] focus:border-[#6366F1] transition-colors"
            />
          </div>
          <div>
            <label className="block text-sm mb-1 text-[#F3F4F6]/80">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-[#6366F1]/30 bg-[#0D1117]/50 text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#6366F1] focus:border-[#6366F1] transition-colors"
            />
          </div>
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button
            type="submit"
            className="w-full mt-2 px-4 py-2 rounded-lg bg-[#6366F1] text-white shadow hover:glow-indigo-intense hover:scale-[1.01] transition-all duration-300"
          >
            Sign In
          </button>
        </form>
        <p className="mt-4 text-sm text-[#F3F4F6]/60">
          Don't have an account?{" "}
          <Link to="/signup" className="text-[#6366F1] hover:text-[#7C3AED] transition-colors">Create your account</Link>
        </p>
        <p className="mt-2 text-sm text-[#F3F4F6]/60">
          <Link to="/" className="text-[#6366F1] hover:text-[#7C3AED] transition-colors">← Back to home</Link>
        </p>
      </motion.div>
    </div>
  );
}

