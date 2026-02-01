import { Navigate } from "react-router-dom";
import { useAuth } from "./useAuth";

export default function ProtectedRoute({ children, role }) {
  const { isAuth, user } = useAuth();

  if (!isAuth) return <Navigate to="/login" />;
  if (role && user.role !== role) return <Navigate to="/404" />;

  return children;
}
