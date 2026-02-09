import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function ActivityLog() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    api.get("/admin/activity/")
      .then((res) => setLogs(res.data));
  }, []);

  return (
    <div className="glass-card">
      <h2>🧾 Activity Log</h2>

      {logs.map((l, i) => (
        <div key={i}>
          {l.action} – {l.timestamp}
        </div>
      ))}
    </div>
  );
}
