import { NavLink, useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../auth/AuthContext";
import { useTheme } from "../theme/ThemeContext";
import "./MainLayout.css";

const MainLayout = ({ children }) => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const { toggleTheme, theme } = useTheme();
  
  // ✅ State for collapsing sidebar
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      {/* ✅ Dynamic Class: If collapsed, add 'collapsed' class 
         This triggers the CSS width change.
      */}
      <aside className={`sidebar glass ${isCollapsed ? "collapsed" : ""}`}>
        
        {/* Toggle Button */}
        <button 
          className="sidebar-toggle" 
          onClick={() => setIsCollapsed(!isCollapsed)}
          title={isCollapsed ? "Expand" : "Collapse"}
        >
          {isCollapsed ? "→" : "←"}
        </button>

        <div className="sidebar-header">
          {/* Hide full title when collapsed */}
          <h3>{isCollapsed ? "📚" : "📚 Gyaan"}</h3>
        </div>
        
        <div className="sidebar-links">
          {/* ADMIN LINKS */}
          {user?.role === "ADMIN" && (
            <>
              <NavLink to="/admin" end title="Dashboard">
                <span className="icon">📊</span>
                {!isCollapsed && <span className="link-text">Dashboard</span>}
              </NavLink>
              <NavLink to="/admin/books" title="Books">
                <span className="icon">📖</span>
                {!isCollapsed && <span className="link-text">Books</span>}
              </NavLink>
              <NavLink to="/admin/issues" title="Issues">
                <span className="icon">📑</span>
                {!isCollapsed && <span className="link-text">Issues</span>}
              </NavLink>
              <NavLink to="/admin/penalties" title="Penalties">
                <span className="icon">💸</span>
                {!isCollapsed && <span className="link-text">Penalties</span>}
              </NavLink>
            </>
          )}

          {/* BORROWER LINKS */}
          {user?.role === "BORROWER" && (
            <>
              <NavLink to="/borrower" end title="Dashboard">
                <span className="icon">📊</span>
                {!isCollapsed && <span className="link-text">Dashboard</span>}
              </NavLink>
              <NavLink to="/borrower/books" title="Browse Books">
                <span className="icon">🔍</span>
                {!isCollapsed && <span className="link-text">Browse</span>}
              </NavLink>
              <NavLink to="/borrower/issues" title="My Books">
                <span className="icon">📚</span>
                {!isCollapsed && <span className="link-text">My Books</span>}
              </NavLink>
              <NavLink to="/borrower/penalties" title="My Fines">
                <span className="icon">💰</span>
                {!isCollapsed && <span className="link-text">My Fines</span>}
              </NavLink>
            </>
          )}
        </div>

        {/* Footer with Theme Toggle */}
        <div className="sidebar-footer">
          <button onClick={toggleTheme} className="theme-btn" title="Switch Theme">
             {theme === 'light' ? (isCollapsed ? '🌙' : '🌙 Dark') : (isCollapsed ? '☀️' : '☀️ Light')}
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="content-wrapper">
        <header className="top-nav glass">
          <div className="user-info">
             Welcome, <strong>{user?.email}</strong>
          </div>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </header>

        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;