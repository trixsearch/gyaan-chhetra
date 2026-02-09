import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";
import { toast } from "react-toastify";

const AddBook = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    writer: "",
    genre: "",
    quantity: 1,
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/admin/books/", {
        ...form,
        genre: [form.genre],
      });

      toast.success("Book added successfully");
      navigate("/admin/books");
    } catch (err) {
      toast.error("Failed to add book");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h2>➕ Add Book</h2>

      <input name="title" placeholder="Title" onChange={handleChange} required />
      <input name="writer" placeholder="Writer" onChange={handleChange} required />
      <input name="genre" placeholder="Genre" onChange={handleChange} required />
      <input
        name="quantity"
        type="number"
        min="1"
        onChange={handleChange}
        required
      />

      <button type="submit">Save</button>
    </form>
  );
};

const styles = {
  form: {
    maxWidth: "400px",
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
};

export default AddBook;
