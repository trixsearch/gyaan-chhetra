import { useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

export default function AddBorrower() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/admin/accounts/borrowers/", {
        email,
        password,
      });
      toast.success("Borrower created");
      setEmail("");
      setPassword("");
    } catch {
      toast.error("Failed to create borrower");
    }
  };

  return (
    <form onSubmit={submit} className="glass">
      <h3>Add Borrower</h3>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button>Add</button>
    </form>
  );
}
