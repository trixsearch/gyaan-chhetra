import { Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./AuthContext";

const ProtectedRoute = ({ children, role }) => {
  const { isAuth, user } = useContext(AuthContext);

  // 🔴 Not logged in
  if (!isAuth) {
    return <Navigate to="/login" replace />;
  }

  // ⏳ Wait until user is loaded
  if (!user) {
    return null; // or a loading spinner
  }

  // 🚫 Role mismatch → redirect to Unauthorized page
  if (role && user.role !== role) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

export default ProtectedRoute;