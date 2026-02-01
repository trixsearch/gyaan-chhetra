import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { ThemeProvider } from "./context/ThemeContext";
import { AuthProvider } from "./auth/AuthContext"; // ✅ Added AuthProvider
import { ToastContainer } from "react-toastify";   // ✅ Added Toast components
import "react-toastify/dist/ReactToastify.css";    // ✅ Added Toast styles
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider>
      {/* AuthProvider wraps the App so we can check login status anywhere */}
      <AuthProvider>
        <App />
        {/* ToastContainer shows the popup alerts */}
        <ToastContainer position="top-right" />
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);