import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/axios";

export default function BorrowerDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get("/borrower/issues/my-books/")
      .then(res => setData(res.data))
      .catch(() => console.error("Failed to load dashboard"));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h2>📚 My Dashboard</h2>

      {data && (
        <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem" }}>
          <Card title="My Books" value={data.issues.length} />
          <Card title="Total Penalty (₹)" value={data.total_penalty} highlight={data.total_penalty > 0} />
        </div>
      )}

      <ul>
        <li><Link to="/borrower/books">Browse Books</Link></li>
        <li><Link to="/borrower/my-books">Meri Issued Books</Link></li>
        <li><Link to="/borrower/penalties">My Penalties</Link></li>
      </ul>
    </div>
  );
}

const Card = ({ title, value, highlight }) => (
  <div
    style={{
      padding: "1rem",
      borderRadius: "10px",
      minWidth: "180px",
      background: highlight ? "#ffe5e5" : "#f4f4f4",
      border: highlight ? "1px solid red" : "1px solid #ddd",
    }}
  >
    <h4>{title}</h4>
    <h2>{value}</h2>
  </div>
);
