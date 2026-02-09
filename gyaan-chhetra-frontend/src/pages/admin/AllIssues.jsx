import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

export default function AllIssues() {
  const [issues, setIssues] = useState([]);

  useEffect(() => {
    loadIssues();
  }, []);

  const loadIssues = async () => {
    try {
      const res = await api.get("/admin/issues/");
      setIssues(res.data);
    } catch {
      toast.error("Failed to load issues");
    }
  };

  return (
    <div>
      <h2>📚 All Book Issues</h2>

      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Book</th>
            <th>Status</th>
            <th>Due</th>
          </tr>
        </thead>
        <tbody>
          {issues.map(i => (
            <tr key={i.uuid}>
              <td>{i.user.email}</td>
              <td>{i.book.title}</td>
              <td>
                <span className={`badge ${i.status.toLowerCase()}`}>
                  {i.status}
                </span>
              </td>
              <td>{i.due_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
