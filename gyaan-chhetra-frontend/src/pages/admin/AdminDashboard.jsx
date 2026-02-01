import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";
import BookForm from "../../components/BookForm.jsx";
import BookList from "../../components/BookList.jsx";

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

  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <>
      <h2>📚 Book Management</h2>

      <BookForm onSuccess={fetchBooks} />

      <BookList
        books={books}
        loading={loading}
        onDelete={fetchBooks}
      />
    </>
  );
};

export default AdminDashboard;
