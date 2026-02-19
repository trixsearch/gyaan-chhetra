import Skeleton from "./Skeleton";
import api from "../api/axios";
import { toast } from "react-toastify";

const BookList = ({ books, loading, onDelete }) => {
  const remove = async (id) => {
    try {
      await api.delete(`/admin/books/${id}/`);
      toast.success("Book deleted");
      onDelete();
    } catch {
      toast.error("Delete failed");
    }
  };

  if (loading) {
    return (
      <>
        <Skeleton height={30} />
        <Skeleton height={30} />
      </>
    );
  }

  return (
    <div>
      {books.map((book) => (
        <div
          key={book.uuid}
          className="glass"
          style={{
            padding: 16,
            marginTop: 10,
            border:
              book.available_quantity === 0
                ? "1px solid red"
                : "1px solid #e0e0e0",
            background:
              book.available_quantity === 0
                ? "#ffe5e5"
                : "#fafafa",
            borderRadius: "8px",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <div>
              <strong>{book.title}</strong> — {book.writer}
              <br />
              Total Qty: {book.quantity}
              <br />
              Available: {book.available_quantity}
            </div>

            <button
              onClick={() => remove(book.uuid)}
              style={{
                background: "red",
                color: "white",
                border: "none",
                padding: "6px 10px",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              ❌ Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default BookList;
