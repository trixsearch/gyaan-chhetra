import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [q, setQ] = useState("");

  return (
    <input
      placeholder="Search books..."
      value={q}
      onChange={e => {
        setQ(e.target.value);
        onSearch(e.target.value);
      }}
      style={{ padding: "0.5rem", width: "100%", marginBottom: "1rem" }}
    />
  );
}
