import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Login from "./pages/Login";
import ProtectedRoute from "./auth/ProtectedRoute";
import MainLayout from "./layout/MainLayout";
import NotFound from "./pages/NotFound";
import Unauthorized from "./pages/Unauthorized";
import AdminIssues from "./pages/admin/AdminIssues";

// Admin Pages
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminBooks from "./pages/admin/AdminBooks";
import AddBook from "./pages/admin/AddBook";
import AddBorrower from "./pages/admin/AddBorrower";

// ✅ Import Penalties (Ensure this matches your actual filename: Penalties.jsx or AdminPenalties.jsx)
// We are importing it as "AdminPenalties" to use inside the JSX below.
import AdminPenalties from "./pages/admin/Penalties";

// Borrower Pages
import BorrowerDashboard from "./pages/borrower/BorrowerDashboard";
import BorrowerBooks from "./pages/borrower/BorrowerBooks";
import BorrowerMyBooks from "./pages/borrower/BorrowerMyBooks";

const pageVariants = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -10 },
};

// Helper component to apply animation to any page
const AnimatedPage = ({ children }) => (
  <motion.div
    variants={pageVariants}
    initial="initial"
    animate="animate"
    exit="exit"
    style={{ width: "100%", height: "100%" }}
  >
    {children}
  </motion.div>
);

export default function App() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        {/* 🔓 Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* 🟦 ADMIN SECTION */}
        <Route
          path="/admin/*"
          element={
            <ProtectedRoute role="ADMIN">
              <MainLayout>
                <AnimatedPage>
                  <Routes>
                    <Route index element={<AdminDashboard />} />

                    {/* Books */}
                    <Route path="books" element={<AdminBooks />} />
                    <Route path="books/add" element={<AddBook />} />

                    {/* Borrowers */}
                    <Route path="borrowers" element={<AddBorrower />} />
                    <Route path="borrowers/add" element={<AddBorrower />} />

                    {/* Penalties */}
                    <Route path="penalties" element={<AdminPenalties />} />

                    {/* Catch-all */}
                    <Route path="*" element={<NotFound />} />
                    <Route
                      path="issues"
                      element={
                        <AnimatedPage>
                          <AdminIssues />
                        </AnimatedPage>
                      }
                    />
                  </Routes>
                </AnimatedPage>
              </MainLayout>
            </ProtectedRoute>
          }
        />

        {/* 🟩 BORROWER SECTION */}
        <Route
          path="/borrower/*"
          element={
            <ProtectedRoute role="BORROWER">
              <MainLayout>
                <AnimatedPage>
                  <Routes>
                    <Route index element={<BorrowerDashboard />} />
                    <Route path="books" element={<BorrowerBooks />} />
                    <Route path="my-books" element={<BorrowerMyBooks />} />

                    {/* Catch-all */}
                    <Route path="*" element={<NotFound />} />
                  </Routes>
                </AnimatedPage>
              </MainLayout>
            </ProtectedRoute>
          }
        />

        {/* Global Catch-all */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AnimatePresence>
  );
}
