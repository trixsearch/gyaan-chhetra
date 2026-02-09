import { createContext, useContext, useState, useEffect } from "react";

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  // 1. Check local storage, default to 'dark'
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "dark");

  useEffect(() => {
    // 2. This is the fix: Apply class to the <body> tag directly
    const root = document.body;
    
    // Remove old class to prevent conflicts
    root.classList.remove("light-theme", "dark-theme");

    if (theme === "light") {
      root.classList.add("light-theme");
    } else {
      root.classList.add("dark-theme");
    }

    // Save to local storage
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  return (
    // 3. Pass 'theme' string so buttons can show "Dark" or "Light" text
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);