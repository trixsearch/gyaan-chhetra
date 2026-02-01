import { Routes, Route } from "react-router-dom";
import { motion } from "framer-motion";
import Login from "./pages/Login";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./auth/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h1>Dashboard</h1>
              </motion.div>
            </MainLayout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
