import { useState } from "react";
import api from "../api/axios";
import { toast } from "react-toastify";

const IssueBookForm = ({ onSuccess }) => {
  const [form, setForm] = useState({
    borrower_email: "",
    book_uuid: "",
    due_date: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/admin/issues/", form);
      toast.success("Book issued successfully");
      setForm({ borrower_email: "", book_uuid: "", due_date: "" });
      onSuccess?.();
    } catch {
      toast.error("Failed to issue book");
    }
  };

  return (
    <form className="glass-card" onSubmit={handleSubmit}>
      <h3>Issue Book</h3>

      <input
        placeholder="Borrower Email"
        value={form.borrower_email}
        onChange={(e) =>
          setForm({ ...form, borrower_email: e.target.value })
        }
        required
      />

      <input
        placeholder="Book UUID"
        value={form.book_uuid}
        onChange={(e) =>
          setForm({ ...form, book_uuid: e.target.value })
        }
        required
      />

      <input
        type="date"
        value={form.due_date}
        onChange={(e) =>
          setForm({ ...form, due_date: e.target.value })
        }
        required
      />

      <button type="submit">Issue</button>
    </form>
  );
};

export default IssueBookForm;
