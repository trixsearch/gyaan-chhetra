import { useState } from "react";
import api from "../api/axios";
import { toast } from "react-toastify";

const BookForm = ({ onSuccess }) => {
  const [form, setForm] = useState({
    title: "",
    writer: "",
    genre: "",
    quantity: 1,
  });

  const submit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/admin/books/", {
        ...form,
        genre: form.genre.split(",").map(g => g.trim()),
      });

      toast.success("Book added");
      setForm({ title: "", writer: "", genre: "", quantity: 1 });
      onSuccess();
    } catch {
      toast.error("Failed to add book");
    }
  };

  return (
    <form className="glass" onSubmit={submit} style={{ padding: 16 }}>
      <h3>Add Book</h3>

      <input
        placeholder="Title"
        value={form.title}
        onChange={e => setForm({ ...form, title: e.target.value })}
        required
      />

      <input
        placeholder="Writer"
        value={form.writer}
        onChange={e => setForm({ ...form, writer: e.target.value })}
        required
      />

      <input
        placeholder="Genre (comma separated)"
        value={form.genre}
        onChange={e => setForm({ ...form, genre: e.target.value })}
      />

      <input
        type="number"
        min="1"
        value={form.quantity}
        onChange={e => setForm({ ...form, quantity: +e.target.value })}
      />

      <button type="submit">Add</button>
    </form>
  );
};

export default BookForm;
