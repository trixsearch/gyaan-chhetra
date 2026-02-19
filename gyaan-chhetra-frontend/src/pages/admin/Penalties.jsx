import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function Penalties() {
  const [penalties, setPenalties] = useState([]);

  useEffect(() => {
    api.get("/admin/penalties/")
      .then(res => setPenalties(res.data))
      .catch(() => console.error("Failed to load penalties"));
  }, []);

  return (
    <div>
      <h2>💸 Penalties</h2>

      {penalties.length === 0 ? (
        <p>No penalties</p>
      ) : (
        <table className="glass">
          <thead>
            <tr>
              <th>Borrower</th>
              <th>Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {penalties.map(p => (
              <tr key={p.id}>
                <td>{p.issue.borrower_email}</td>
                <td>₹{p.amount}</td>
                <td>{p.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
