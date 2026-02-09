import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

export default function AdminPenalties() {
  const [penalties, setPenalties] = useState([]);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const res = await api.get("/admin/penalties/");
      setPenalties(res.data);
    } catch {
      toast.error("Failed to load penalties");
    }
  };

  return (
    <div>
      <h2>💰 Penalties</h2>

      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Book</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {penalties.map(p => (
            <tr key={p.uuid}>
              <td>{p.user.email}</td>
              <td>{p.book.title}</td>
              <td>₹{p.amount}</td>
              <td>{p.is_paid ? "Paid" : "Unpaid"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
