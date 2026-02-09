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
          {/* ✅ UPDATED ADMIN SECTION */}
          {user?.role === "ADMIN" && (
            <>
              <NavLink to="/admin" end>
                Dashboard
              </NavLink>
              <NavLink to="/admin/books">Books</NavLink>
            </>
          )}

          {user?.role === "BORROWER" && (
            <>
              <NavLink to="/borrower">Borrower Dashboard</NavLink>
              <NavLink to="/borrower/books">Books</NavLink>
            </>
          )}

          <button onClick={toggleTheme} className="theme-btn">
            🌓 Chhaya
          </button>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </nav>

      <main className="page">{children}</main>
    </div>
  );
};

export default MainLayout;
