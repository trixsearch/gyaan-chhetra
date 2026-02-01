import { useState } from "react";
import api from "../api/axios";
import { useAuth } from "../auth/useAuth";
import { toast } from "react-toastify";

export default function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async e => {
    e.preventDefault();
    const res = await api.post("/accounts/login/", {
      email,
      password,
    });

    login(res.data.access, res.data.user);
    toast.success("Logged in");
  };

  return (
    <form className="glass" style={styles.form} onSubmit={submit}>
      <h2>Login</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button className="btn">Login</button>
    </form>
  );
}

const styles = {
  form: {
    maxWidth: 350,
    margin: "6rem auto",
    padding: "2rem",
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
};
