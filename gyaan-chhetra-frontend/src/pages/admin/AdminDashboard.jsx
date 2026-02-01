import { Link } from "react-router-dom";

export default function AdminDashboard() {
  return (
    <div className="glass" style={{ padding: "2rem" }}>
      <h2>Admin Dashboard</h2>

      <ul style={{ marginTop: "1rem", lineHeight: 2 }}>
        <li><Link to="/admin/books">Manage Books</Link></li>
        <li><Link to="/admin/borrowers">Manage Borrowers</Link></li>
      </ul>
    </div>
  );
}
