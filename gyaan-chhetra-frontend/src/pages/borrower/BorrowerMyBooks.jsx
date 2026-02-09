import { useEffect, useState } from "react";
import api from "../../api/axios";
import { toast } from "react-toastify";

const BorrowerMyBooks = () => {
  const [issues, setIssues] = useState([]);

  const fetchIssues = async () => {
    try {
      // Make sure your API returns 'days_left' in the response!
      const res = await api.get("/borrower/issues/");
      setIssues(res.data.results || res.data);
    } catch {
      toast.error("Failed to load issued books");
    }
  };

  const returnBook = async (issue_uuid) => {
    try {
      await api.post(`/borrower/issues/${issue_uuid}/return/`);
      toast.success("Book returned successfully");
      fetchIssues(); // Refresh list
    } catch {
      toast.error("Return failed");
    }
  };

  useEffect(() => {
    fetchIssues();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">📖 Meri Issued Books</h2>

      {issues.length === 0 ? (
        <p className="text-gray-500">You haven't borrowed any books yet.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {issues.map((issue) => (
            <div key={issue.uuid} className="glass-card p-4 border rounded shadow-sm">
              <h3 className="text-xl font-semibold">{issue.book_title}</h3>
              
              <p className="mt-2"
                style={{
                  color: issue.is_overdue ? "red" : "inherit",
                  fontWeight: issue.is_overdue ? "bold" : "normal",
                }}
              >
                Due: {issue.due_date}
                {issue.is_overdue && " ⚠ OVERDUE"}
              </p>

              {/* ✅ ADDED: Due Soon Warning */}
              {issue.days_left <= 2 && !issue.is_overdue && (
                <p style={{ color: "orange", fontWeight: "bold", marginTop: "5px" }}>
                  ⏰ Due Soon!
                </p>
              )}

              {issue.penalty_amount > 0 && (
                <p style={{ color: "crimson", marginTop: "5px" }}>
                  Penalty: ₹{issue.penalty_amount}
                </p>
              )}

              <button 
                onClick={() => returnBook(issue.uuid)}
                className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
              >
                Return Book
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BorrowerMyBooks;