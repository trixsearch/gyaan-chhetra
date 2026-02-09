export default function SearchBox({ value, onChange }) {
    return (
      <input
        placeholder="Search books..."
        value={value}
        onChange={e => onChange(e.target.value)}
        style={{ marginBottom: "1rem", width: "100%" }}
      />
    );
  }
  