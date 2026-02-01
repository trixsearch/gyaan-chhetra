import { Routes, Route, Navigate } from "react-router-dom";
import { motion } from "framer-motion";
import Login from "./pages/Login";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./auth/ProtectedRoute";

// ✅ Import your new Dashboard pages
// (Make sure you create these files in src/pages/ if they don't exist yet!)
import AdminDashboard from "./pages/admin/AdminDashboard";
import BorrowerDashboard from "./pages/borrower/BorrowerDashboard";

export default function App() {
  return (
    <Routes>
      {/* Public Route */}
      <Route path="/login" element={<Login />} />

      {/* Redirect root "/" to login or a specific dashboard */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      {/* 🛡️ ADMIN ROUTE */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute role="ADMIN">
            <MainLayout>
              <AdminDashboard />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* 🛡️ BORROWER ROUTE */}
      <Route
        path="/borrower"
        element={
          <ProtectedRoute role="BORROWER">
            <MainLayout>
              <BorrowerDashboard />
            </MainLayout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}