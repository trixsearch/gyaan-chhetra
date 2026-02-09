import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

const BorrowerBooks = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const res = await api.get("/books/");
      setBooks(res.data);
    } catch {
      toast.error("Failed to load books");
    }
  };

  return (
    <div>
      <h2>📚 Available Books</h2>

      <table width="100%">
        <thead>
          <tr>
            <th>Title</th>
            <th>Writer</th>
            <th>Available</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {books.map((b) => (
            <tr key={b.uuid}>
              <td>{b.title}</td>
              <td>{b.writer}</td>
              <td>{b.available_quantity}</td>
              <td>
                <BorrowButton book={b} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const BorrowButton = ({ book }) => {
  const handleBorrow = async () => {
    try {
      await api.post("/borrower/issues/", {
        book_uuid: book.uuid,
      });
      toast.success("Book borrowed");
    } catch {
      toast.error("Borrow failed");
    }
  };

  return (
    <button disabled={book.available_quantity < 1} onClick={handleBorrow}>
      Borrow
    </button>
  );
};

export default BorrowerBooks;
