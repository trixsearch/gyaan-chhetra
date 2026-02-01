import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import api from "../api/axios";
import { AuthContext } from "../auth/AuthContext";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    role: "ADMIN",
  });

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      const res = await api.post("/accounts/login/", formData);

      // ✅ FIX START: Explicitly save tokens for the Interceptor
      // The interceptor in api/axios.js looks specifically for "access"
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      // ✅ FIX END

      // Update the global Auth Context state
      login(res.data.access, res.data.user);

      toast.success("Login successful");

      if (res.data.user.role === "ADMIN") {
        navigate("/admin");
      } else {
        navigate("/borrower");
      }
    } catch (err) {
      console.error(err);
      toast.error("Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="glass-card">
        <h2>Login</h2>

        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
          required
        />

        <select
          value={formData.role}
          onChange={(e) =>
            setFormData({ ...formData, role: e.target.value })
          }
        >
          <option value="ADMIN">Admin</option>
          <option value="BORROWER">Borrower</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
};

export default Login;