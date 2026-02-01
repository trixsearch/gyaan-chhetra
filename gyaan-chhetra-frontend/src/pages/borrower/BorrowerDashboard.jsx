import { Link } from "react-router-dom";

export default function BorrowerDashboard() {
  return (
    <div className="glass" style={{ padding: "2rem" }}>
      <h2>Mera Dashboard</h2>

      <ul style={{ marginTop: "1rem" }}>
        <li><Link to="/borrower/books">Browse Books</Link></li>
        <li><Link to="/borrower/my-books">Meri Issued Books</Link></li>
      </ul>
    </div>
  );
}
