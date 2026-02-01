import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function MyBooks() {
  const [issues, setIssues] = useState([]);

  useEffect(() => {
    api.get("/borrower/issues/")
      .then(res => setIssues(res.data));
  }, []);

  return (
    <div className="glass" style={{ padding: "2rem" }}>
      <h3>My Issued Books</h3>

      {issues.map(i => (
        <div key={i.uuid}>
          {i.book_title} – Due: {i.due_date}
        </div>
      ))}
    </div>
  );
}
