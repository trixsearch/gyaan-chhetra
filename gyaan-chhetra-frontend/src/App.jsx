import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Login from "./pages/Login";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./auth/ProtectedRoute";
import AdminDashboard from "./pages/admin/AdminDashboard";
import BorrowerDashboard from "./pages/borrower/BorrowerDashboard";

const pageVariants = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -10 },
};

export default function App() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" />} />

        <Route
          path="/admin"
          element={
            <ProtectedRoute role="ADMIN">
              <MainLayout>
                <motion.div
                  variants={pageVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                >
                  <AdminDashboard />
                </motion.div>
              </MainLayout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/borrower"
          element={
            <ProtectedRoute role="BORROWER">
              <MainLayout>
                <motion.div
                  variants={pageVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                >
                  <BorrowerDashboard />
                </motion.div>
              </MainLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </AnimatePresence>
  );
}
