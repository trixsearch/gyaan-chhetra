import { Link } from "react-router-dom";

export default function Unauthorized() {
  return (
    <div style={{ padding: "3rem", textAlign: "center" }}>
      <h1>🚫 Unauthorized</h1>
      <p>You don’t have access to this page</p>
      <Link to="/login">Login again</Link>
    </div>
  );
}
