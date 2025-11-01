import { createContext, useContext, useEffect, useMemo, useState } from "react";
import bcrypt from "bcryptjs";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const raw = localStorage.getItem("ns_user");
    if (raw) setUser(JSON.parse(raw));
  }, []);

  const signIn = async (email, password) => {
    const raw = localStorage.getItem("ns_user");
    if (!raw) throw new Error("No account found");
    const saved = JSON.parse(raw);
    const ok = await bcrypt.compare(password, saved.hash);
    if (!ok) throw new Error("Invalid credentials");
    setUser({ email });
    return true;
  };

  const signUp = async (email, password) => {
    const salt = bcrypt.genSaltSync(10);
    const hash = bcrypt.hashSync(password, salt);
    const payload = { email, hash, createdAt: Date.now() };
    localStorage.setItem("ns_user", JSON.stringify(payload));
    setUser({ email });
    return true;
  };

  const signOut = () => {
    setUser(null);
    localStorage.removeItem("ns_user");
  };

  const value = useMemo(() => ({ user, signIn, signUp, signOut }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

