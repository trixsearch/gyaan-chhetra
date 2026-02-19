import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

export default function Borrowers() {
  const [borrowers, setBorrowers] = useState([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const fetchBorrowers = async () => {
    const res = await api.get("/admin/borrowers/");
    setBorrowers(res.data);
  };

  const handleAdd = async () => {
    try {
      await api.post("/admin/borrowers/add/", { email, password });
      toast.success("Borrower added");
      setEmail("");
      setPassword("");
      fetchBorrowers();
    } catch (err) {
      toast.error(err.response?.data?.error || "Error");
    }
  };

  useEffect(() => {
    fetchBorrowers();
  }, []);

  return (
    <div>
      <h2>👤 Borrowers</h2>

      <div>
        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleAdd}>Add</button>
      </div>

      <ul>
        {borrowers.map((b) => (
          <li key={b.id}>{b.email}</li>
        ))}
      </ul>
    </div>
  );
}
