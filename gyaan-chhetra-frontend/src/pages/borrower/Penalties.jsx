import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function BorrowerPenalties() {
  const [penalties, setPenalties] = useState([]);

  useEffect(() => {
    api.get("/borrower/penalties/")
      .then(res => setPenalties(res.data))
      .catch(() => console.error("Failed to load penalties"));
  }, []);

  return (
    <div>
      <h2>💰 My Penalties</h2>

      {penalties.length === 0 ? (
        <p>No penalties 🎉</p>
      ) : (
        <ul>
          {penalties.map(p => (
            <li key={p.id}>
              ₹{p.amount} — {p.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
