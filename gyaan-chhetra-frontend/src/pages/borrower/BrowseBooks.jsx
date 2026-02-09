import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

export default function BrowseBooks() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    api.get("/books/")
      .then((res) => setBooks(res.data.results || res.data))
      .catch(() => toast.error("Failed to load books"));
  }, []);

  return (
    <div className="glass-card">
      <h2>📚 Available Books</h2>

      {books.map((b) => (
        <div key={b.uuid} className="book-row">
          <strong>{b.title}</strong> – {b.writer}
          <span> ({b.available_quantity} available)</span>
        </div>
      ))}
    </div>
  );
}
