import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

const Penalties = () => {
  const [penalties, setPenalties] = useState([]);

  useEffect(() => {
    fetchPenalties();
  }, []);

  const fetchPenalties = async () => {
    try {
      const res = await api.get("/borrower/penalties/");
      setPenalties(res.data);
    } catch {
      toast.error("Failed to load penalties");
    }
  };

  return (
    <div>
      <h2>💸 Penalties</h2>

      {penalties.length === 0 ? (
        <p>No penalties 🎉, Chill Kar</p>
      ) : (
        <table width="100%">
          <thead>
            <tr>
              <th>Book</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {penalties.map((p) => (
              <tr key={p.uuid}>
                <td>{p.book.title}</td>
                <td>₹{p.amount}</td>
                <td>{p.is_paid ? "Paid" : "Unpaid"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Penalties;
