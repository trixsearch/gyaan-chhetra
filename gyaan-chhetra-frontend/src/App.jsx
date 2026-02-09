import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Login from "./pages/Login";
import ProtectedRoute from "./auth/ProtectedRoute";
import AdminDashboard from "./pages/admin/AdminDashboard";
import BorrowerDashboard from "./pages/borrower/BorrowerDashboard";
import AdminLayout from "./layout/AdminLayout";

// admin pages
import AdminBooks from "./pages/admin/AdminBooks";
import AddBook from "./pages/admin/AddBook";

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

        {/* 🟦 ADMIN ROUTES */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute role="ADMIN">
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          <Route
            index
            element={
              <motion.div {...pageVariants}>
                <AdminDashboard />
              </motion.div>
            }
          />

          <Route
            path="books"
            element={
              <motion.div {...pageVariants}>
                <AdminBooks />
              </motion.div>
            }
          />

          <Route
            path="books/add"
            element={
              <motion.div {...pageVariants}>
                <AddBook />
              </motion.div>
            }
          />
        </Route>

        {/* 🟩 BORROWER ROUTES */}
        <Route
          path="/borrower"
          element={
            <ProtectedRoute role="BORROWER">
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          {/* 1. Dashboard (Route is /borrower) */}
          <Route
            index
            element={
              <motion.div {...pageVariants}>
                <BorrowerDashboard />
              </motion.div>
            }
          />
          {/* 2. Books (Route becomes /borrower/books automatically) */}
          <Route
            path="/books"
            element={
              <ProtectedRoute role="BORROWER">
                <MainLayout>
                  <BorrowerBooks />
                </MainLayout>
              </ProtectedRoute>
            }
          />
        </Route>
      </Routes>
    </AnimatePresence>
  );
}
