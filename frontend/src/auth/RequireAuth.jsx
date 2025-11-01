import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@/auth/AuthContext";

export default function RequireAuth({ children }) {
  const { user } = useAuth();
  const location = useLocation();
  if (!user) {
    return <Navigate to="/signin" state={{ from: location }} replace />;
  }
  return children;
}

