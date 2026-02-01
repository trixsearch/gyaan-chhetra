import { Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "./AuthContext";

const ProtectedRoute = ({ children, role }) => {
  const { isAuth, user } = useContext(AuthContext);

  // Not logged in
  if (!isAuth) {
    return <Navigate to="/login" replace />;
  }

  // Role mismatch
  if (role && user?.role !== role) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
