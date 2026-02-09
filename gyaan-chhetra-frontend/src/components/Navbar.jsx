import { NavLink, useNavigate } from "react-router-dom";
import { useTheme } from "../theme/ThemeContext";
import { useContext } from "react";
import { AuthContext } from "../auth/AuthContext";
import "./Navbar.css"; // Ensure you create this file

export default function Navbar() {
  const { toggleTheme, theme } = useTheme();
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar glass">
      <div className="brand">
        <span className="logo">📚</span>
        <h1>Gyaan Chhetra</h1>
      </div>

      <div className="nav-links">
        <NavLink
          to="/admin"
          end
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/admin/borrowers"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Borrowers
        </NavLink>
        <NavLink
          to="/admin/penalties"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Penalties
        </NavLink>
        <NavLink to="/admin/borrowers/add">Add Borrower</NavLink>
      </div>

      <div className="nav-actions">
        <button
          className="theme-toggle"
          onClick={toggleTheme}
          title="Toggle Theme"
        >
          {theme === "light" ? "🌙" : "☀️"}
        </button>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
}
