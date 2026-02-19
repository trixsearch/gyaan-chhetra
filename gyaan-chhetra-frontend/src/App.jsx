import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";

import Login from "./pages/Login";
import ProtectedRoute from "./auth/ProtectedRoute";
import MainLayout from "./layout/MainLayout";
import NotFound from "./pages/NotFound";
import Unauthorized from "./pages/Unauthorized";

// Admin pages
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminBooks from "./pages/admin/AdminBooks";
import AdminIssues from "./pages/admin/AdminIssues";
import Penalties from "./pages/admin/Penalties";
import AddBorrower from "./pages/admin/AddBorrower";

// Borrower pages
import BorrowerDashboard from "./pages/borrower/BorrowerDashboard";
import BorrowerBooks from "./pages/borrower/BorrowerBooks";
import BorrowerMyBooks from "./pages/borrower/BorrowerMyBooks";
import BorrowerPenalties from "./pages/borrower/Penalties";

const AnimatedPage = ({ children }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -10 }}
  >
    {children}
  </motion.div>
);

export default function App() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        {/* Public */}
        <Route path="/login" element={<Login />} />
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* ADMIN */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute role="ADMIN">
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route
            index
            element={
              <AnimatedPage>
                <AdminDashboard />
              </AnimatedPage>
            }
          />
          <Route
            path="books"
            element={
              <AnimatedPage>
                <AdminBooks />
              </AnimatedPage>
            }
          />
          <Route
            path="issues"
            element={
              <AnimatedPage>
                <AdminIssues />
              </AnimatedPage>
            }
          />
          <Route
            path="penalties"
            element={
              <AnimatedPage>
                <Penalties />
              </AnimatedPage>
            }
          />
          <Route
            path="borrowers"
            element={
              <AnimatedPage>
                <AddBorrower />
              </AnimatedPage>
            }
          />
          <Route
            path="borrowers"
            element={
              <AnimatedPage>
                <AddBorrower />
              </AnimatedPage>
            }
          />
        </Route>

        {/* BORROWER */}
        <Route
          path="/borrower"
          element={
            <ProtectedRoute role="BORROWER">
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route
            index
            element={
              <AnimatedPage>
                <BorrowerDashboard />
              </AnimatedPage>
            }
          />
          <Route
            path="books"
            element={
              <AnimatedPage>
                <BorrowerBooks />
              </AnimatedPage>
            }
          />
          <Route
            path="issues"
            element={
              <AnimatedPage>
                <BorrowerMyBooks />
              </AnimatedPage>
            }
          />
          <Route
            path="penalties"
            element={
              <AnimatedPage>
                <BorrowerPenalties />
              </AnimatedPage>
            }
          />
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AnimatePresence>
  );
}
