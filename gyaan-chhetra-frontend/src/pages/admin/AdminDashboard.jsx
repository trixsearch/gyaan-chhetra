import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";
import BookForm from "../../components/BookForm";
import BookList from "../../components/BookList";
import IssueBookForm from "../../components/IssueBookForm";

const AdminDashboard = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

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

  const [stats, setStats] = useState({
    totalBooks: 0,
    issuedBooks: 0,
    overdueBooks: 0,
  });

  const exportBooks = async () => {
    const res = await api.get("/admin/books/export/", {
      responseType: "blob",
    });
  
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "books.csv");
    document.body.appendChild(link);
    link.click();
  };

  useEffect(() => {
    fetchBooks();
    // ✅ ADDED: Fetch admin stats
    api
      .get("/admin/stats/")
      .then((res) => {
        setStats(res.data);
      })
      .catch(() => {
        console.error("Failed to fetch statistics");
      });
  }, []);

  return (
    <div>
      <h2>📚 Book Management</h2>
      <button onClick={exportBooks}>⬇ Export Books</button>
      <IssueBookForm onSuccess={fetchBooks} />
      <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem" }}>
        <div className="glass-card">📚 Total Books: {stats.totalBooks}</div>
        <div className="glass-card">📕 Issued: {stats.issuedBooks}</div>
        <div className="glass-card">⛔ Overdue: {stats.overdueBooks}</div>
      </div>
      <BookForm onSuccess={fetchBooks} />
      

      <BookList books={books} loading={loading} onDelete={fetchBooks} />
      
    </div>
  );
};

export default AdminDashboard;
