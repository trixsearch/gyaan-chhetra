import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

export default function AdminIssues() {
  const [issues, setIssues] = useState([]);

  const fetchIssues = async () => {
    try {
      const res = await api.get("/admin/issues/");
      setIssues(res.data.results || res.data);
    } catch {
      toast.error("Failed to load issues");
    }
  };

  useEffect(() => {
    fetchIssues();
  }, []);

  return (
    <div>
      <h2>📑 Issued Books</h2>

      {issues.length === 0 ? (
        <p>No active issues</p>
      ) : (
        <table className="glass">
          <thead>
            <tr>
              <th>Book</th>
              <th>Borrower</th>
              <th>Issue Date</th>
              <th>Due Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {issues.map((i) => (
              <tr key={i.uuid}>
                <td>{i.book_title}</td>
                <td>{i.borrower_email}</td>
                <td>{i.issue_date}</td>
                <td>{i.due_date}</td>
                <td>{i.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
