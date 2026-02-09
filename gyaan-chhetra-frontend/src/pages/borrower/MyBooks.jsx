import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function MyBooks() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    api.get("/borrower/issues/")
      .then((res) => setBooks(res.data))
  }, []);

  return (
    <div className="glass-card">
      <h2>📖 Meri Issued Books</h2>

      {books.length === 0 && <p>No books issued</p>}

      {books.map((b) => (
        <div key={b.issue_uuid}>
          {b.book_title} – Due: {b.due_date}
        </div>
      ))}
    </div>
  );
}
