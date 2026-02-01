import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function ManageBorrowers() {
  const [borrowers, setBorrowers] = useState([]);

  useEffect(() => {
    api.get("/admin/accounts/borrowers/")
      .then(res => setBorrowers(res.data));
  }, []);

  return (
    <div className="glass" style={{ padding: "2rem" }}>
      <h3>Borrowers</h3>
      <ul>
        {borrowers.map(b => (
          <li key={b.uuid}>{b.email}</li>
        ))}
      </ul>
    </div>
  );
}
