import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

export default function AdminIssues() {
  const [issues, setIssues] = useState([]);

  const fetchIssues = async () => {
    try {
      const res = await api.get("/admin/issues/");
      setIssues(res.data);
    } catch {
      toast.error("Failed to load issues");
    }
  };

  const handleReturn = async (issueId) => {
    try {
      await api.post(`/admin/issues/${issueId}/return/`);
      toast.success("Book returned");
      fetchIssues(); // refresh list
    } catch {
      toast.error("Return failed");
    }
  };

  useEffect(() => {
    fetchIssues();
  }, []);

  return (
    <div>
      <h2>📑 Issued Books</h2>

      <table className="glass">
        <thead>
          <tr>
            <th>Book</th>
            <th>Borrower</th>
            <th>Due Date</th>
            <th>Status</th>
            <th />
          </tr>
        </thead>

        <tbody>
          {issues.map((i) => (
            <tr key={i.id}>
              <td>{i.book_title}</td>
              <td>{i.borrower_email}</td>
              <td>{i.due_date}</td>
              <td>{i.status}</td>
              <td>
                {i.status === "ISSUED" && (
                  <button onClick={() => handleReturn(i.id)}>
                    Return
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
