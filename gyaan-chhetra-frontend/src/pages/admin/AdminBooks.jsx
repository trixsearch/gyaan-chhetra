import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";

const AdminBooks = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const res = await api.get("/admin/books/");
      setBooks(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const deleteBook = async (uuid) => {
    if (!window.confirm("Delete this book?")) return;

    try {
      await api.delete(`/admin/books/${uuid}/`);
      setBooks((prev) => prev.filter((b) => b.uuid !== uuid));
      toast.success("Book deleted");
    } catch {
      toast.error("Delete failed");
    }
  };

  if (loading) return <p>Loading books...</p>;

  return (
    <div>
      <div style={styles.header}>
        <h2>📚 Books</h2>
        <button onClick={() => navigate("/admin/books/add")}>
          ➕ Add Book
        </button>
      </div>

      <table style={styles.table}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Writer</th>
            <th>Quantity</th>
            <th>Available</th>
          </tr>
        </thead>
        <tbody>
          {books.map((b) => (
            <tr key={b.uuid}>
              <td>{b.title}</td>
              <td>{b.writer}</td>
              <td>{b.quantity}</td>
              <td>{b.available_quantity}</td>
              <td>
                <button onClick={() => deleteBook(b.uuid)}>🗑 Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "1rem",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
  },
};

export default AdminBooks;
