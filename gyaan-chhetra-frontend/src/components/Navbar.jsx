import { useTheme } from "../theme/ThemeContext";

export default function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <nav className="glass" style={styles.nav}>
      <h2 style={styles.logo}>📚 Gyaan Chhetra</h2>

      <div style={styles.actions}>
       <button onClick={toggleTheme}>🌓Roop</button>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "1rem 1.5rem",
    marginBottom: "2rem",
  },
  logo: {
    fontSize: "1.2rem",
    fontWeight: 600,
  },
  actions: {
    display: "flex",
    gap: "1rem",
  },
};
