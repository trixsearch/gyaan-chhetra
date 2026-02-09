import { useEffect, useState } from "react";
import api from "../../api/axios";

const BorrowerBooks = () => {
  const [books, setBooks] = useState([]);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");

  useEffect(() => {
    api
      .get(`/books/?page=${page}&search=${search}`)
      .then((res) => setBooks(res.data.results || res.data));
  }, [page, search]);

  return (
    <div>
      <h2>📚 Browse Books</h2>

      <input
        placeholder="Search book..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginBottom: "1rem" }}
      />

      {books.map((book) => (
        <div key={book.uuid} className="glass-card">
          <b>{book.title}</b>
          <p>Available: {book.available_quantity}</p>
        </div>
      ))}

      <div style={{ marginTop: "1rem" }}>
        <button onClick={() => setPage((p) => Math.max(p - 1, 1))}>
          Prev
        </button>
        <span style={{ margin: "0 1rem" }}>Page {page}</span>
        <button onClick={() => setPage((p) => p + 1)}>Next</button>
      </div>
    </div>
  );
};

export default BorrowerBooks;
