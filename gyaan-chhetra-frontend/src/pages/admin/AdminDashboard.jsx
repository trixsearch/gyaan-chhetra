import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";
import BookForm from "../../components/BookForm";
import BookList from "../../components/BookList";
import IssueBookForm from "../../components/IssueBookForm";

const AdminDashboard = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [recentIssues, setRecentIssues] = useState([]);

  const fetchBooks = async () => {
    try {
      const res = await api.get("/admin/books/");
      setBooks(res.data.results || res.data);
    } catch {
      toast.error("Failed to load books");
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await api.get("/admin/stats/");
      setStats(res.data);
    } catch {
      console.error("Failed to fetch statistics");
    }
  };

  const fetchRecentIssues = async () => {
    try {
      const res = await api.get("/admin/issues/recent/");
      setRecentIssues(res.data);
    } catch {
      console.error("Failed to load recent issues");
    }
  };

  const exportBooks = async () => {
    try {
      const res = await api.get("/admin/books/export/", {
        responseType: "blob",
      });

      const blob = new Blob([res.data], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = "books.csv";
      document.body.appendChild(link);
      link.click();

      link.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      toast.error("Export failed");
    }
  };

  useEffect(() => {
    fetchBooks();
    fetchStats();
    fetchRecentIssues();
  }, []);

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "auto" }}>
      <h1 style={{ marginBottom: "2rem" }}>📊 Admin Dashboard</h1>

      {stats && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "1.5rem",
            marginBottom: "3rem",
          }}
        >
          <StatCard
            title="Total Books"
            value={stats.totalBooks}
            color="#4CAF50"
          />

          <StatCard
            title="Issued Books"
            value={stats.issuedBooks}
            color="#2196F3"
          />

          <StatCard
            title="Overdue"
            value={stats.overdueBooks}
            color="#f44336"
          />

          <StatCard
            title="Borrowers"
            value={stats.totalBorrowers}
            color="#9C27B0"
          />

          <StatCard
            title="Total Penalty (₹)"
            value={stats.totalPenalty}
            color="#FF9800"
          />
        </div>
      )}

      <button
        onClick={exportBooks}
        style={{
          padding: "10px 16px",
          borderRadius: "8px",
          background: "#333",
          color: "white",
          border: "none",
          cursor: "pointer",
          marginBottom: "2rem",
        }}
      >
        ⬇ Export Books
      </button>

      <IssueBookForm onSuccess={fetchBooks} />
      <BookForm onSuccess={fetchBooks} />
      <BookList books={books} loading={loading} onDelete={fetchBooks} />

      <h2 style={{ marginTop: "3rem", marginBottom: "1rem" }}>
  📌 Recent Activity
</h2>

<div
  style={{
    background: "#ffffff",
    padding: "1.5rem",
    borderRadius: "14px",
    boxShadow: "0 8px 25px rgba(0,0,0,0.08)",
    borderLeft: "6px solid #2196F3",
  }}
>
        {recentIssues.length === 0 ? (
          <p>No recent activity</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {recentIssues.map((issue) => (
              <li
              key={issue.uuid}
              style={{
                padding: "10px 0",
                borderBottom: "1px solid #eee",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <span style={{ fontWeight: 600, color: "#333" }}>
                {issue.book_title}
              </span>
            
              <span
                style={{
                  padding: "4px 10px",
                  borderRadius: "20px",
                  fontSize: "0.8rem",
                  background:
                    issue.status === "ISSUED"
                      ? "#e3f2fd"
                      : issue.status === "RETURNED"
                      ? "#e8f5e9"
                      : "#fff3e0",
                  color:
                    issue.status === "ISSUED"
                      ? "#1976d2"
                      : issue.status === "RETURNED"
                      ? "#2e7d32"
                      : "#ef6c00",
                }}
              >
                {issue.status}
              </span>
            </li>
            
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

const StatCard = ({ title, value, color }) => (
  <div
    style={{
      padding: "1.5rem",
      borderRadius: "14px",
      background: "white",
      boxShadow: "0 8px 20px rgba(0,0,0,0.06)",
      borderTop: `5px solid ${color}`,
      transition: "transform 0.2s ease",
    }}
  >
    <p style={{ margin: 0, fontSize: "0.9rem", color: "#666" }}>
      {title}
    </p>
    <h2 style={{ marginTop: "0.5rem", color }}>{value}</h2>
  </div>
);

export default AdminDashboard;
