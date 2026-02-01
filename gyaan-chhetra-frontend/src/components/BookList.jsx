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
      {books.map(book => (
        <div key={book.uuid} className="glass" style={{ padding: 12, marginTop: 8 }}>
          <strong>{book.title}</strong> — {book.writer}
          <br />
          Qty: {book.quantity}
          <button onClick={() => remove(book.uuid)}>❌</button>
        </div>
      ))}
    </div>
  );
};

export default BookList;
