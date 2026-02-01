import { NavLink, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import "./MainLayout.css";
import { useTheme } from "../theme/ThemeContext";


const MainLayout = ({ children }) => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const { toggleTheme } = useTheme();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <nav className="navbar glass">
        <h3>Gyaan Chhetra</h3>

        <div className="nav-links">
          {user?.role === "ADMIN" && (
            <NavLink to="/admin">Admin</NavLink>
          )}

          {user?.role === "BORROWER" && (
            <NavLink to="/borrower">Borrower</NavLink>
          )}
          <button onClick={toggleTheme}>🌓Chhaya</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      <main className="page">{children}</main>
    </div>
  );
};

export default MainLayout;
