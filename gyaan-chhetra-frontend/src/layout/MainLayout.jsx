import { NavLink, useNavigate, Outlet } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../auth/AuthContext";
import { useTheme } from "../theme/ThemeContext";
import "./MainLayout.css";

export default function MainLayout() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const { toggleTheme, theme } = useTheme();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      {/* Sidebar */}
      <aside className={`sidebar glass ${isCollapsed ? "collapsed" : ""}`}>
        <button
          className="sidebar-toggle"
          onClick={() => setIsCollapsed(!isCollapsed)}
        >
          {isCollapsed ? "→" : "←"}
        </button>

        <div className="sidebar-header">
          <h3>{isCollapsed ? "📚" : "📚 Gyaan"}</h3>
        </div>

        <div className="sidebar-links">
          {user?.role === "ADMIN" && (
            <>
              <NavLink to="/admin" end>
                📊 {!isCollapsed && "Dashboard"}
              </NavLink>
              <NavLink to="/admin/books">
                📖 {!isCollapsed && "Books"}
              </NavLink>
              <NavLink to="/admin/issues">
                📑 {!isCollapsed && "Issues"}
              </NavLink>
              <NavLink to="/admin/penalties">
                💸 {!isCollapsed && "Penalties"}
              </NavLink>
              <NavLink to="/admin/borrowers">
                👥 {!isCollapsed && "Borrowers"}
              </NavLink>
            </>
          )}

          {user?.role === "BORROWER" && (
            <>
              <NavLink to="/borrower" end>
                📊 {!isCollapsed && "Dashboard"}
              </NavLink>
              <NavLink to="/borrower/books">
                🔍 {!isCollapsed && "Browse"}
              </NavLink>
              <NavLink to="/borrower/issues">
                📚 {!isCollapsed && "My Books"}
              </NavLink>
              <NavLink to="/borrower/penalties">
                💰 {!isCollapsed && "My Fines"}
              </NavLink>
            </>
          )}
        </div>

        <div className="sidebar-footer">
          <button onClick={toggleTheme}>
            {theme === "light" ? "🌙 Dark" : "☀️ Light"}
          </button>
        </div>
      </aside>

      {/* Content */}
      <div className="content-wrapper">
        <header className="top-nav glass">
          <span>Welcome, {user?.email}</span>
          <button onClick={handleLogout}>Logout</button>
        </header>

        <main className="page-content">
          {/* 🔑 THIS IS CRITICAL */}
          <Outlet />
        </main>
      </div>
    </div>
  );
}
