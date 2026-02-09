import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

const MyIssues = () => {
  const [issues, setIssues] = useState([]);

  useEffect(() => {
    fetchIssues();
  }, []);

  const fetchIssues = async () => {
    try {
      const res = await api.get("/borrower/issues/");
      setIssues(res.data);
    } catch {
      toast.error("Failed to load issued books");
    }
  };

  const returnBook = async (issue_uuid) => {
    try {
      await api.post(`/borrower/issues/${issue_uuid}/return/`);
      toast.success("Book returned");
      fetchIssues();
    } catch {
      toast.error("Return failed");
    }
  };

  return (
    <div>
      <h2>📦 My Issued Books</h2>

      <table width="100%">
        <thead>
          <tr>
            <th>Title</th>
            <th>Issued On</th>
            <th>Due Date</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {issues.map((i) => (
            <tr key={i.uuid}>
              <td>{i.book.title}</td>
              <td>{i.issued_at}</td>
              <td>{i.due_date}</td>
              <td>{i.status}</td>
              <td>
                {i.status === "ISSUED" && (
                  <button onClick={() => returnBook(i.uuid)}>
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
};

export default MyIssues;
