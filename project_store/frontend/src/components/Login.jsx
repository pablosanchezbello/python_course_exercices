import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./../App.css";

function Login({ setEntries }) {
  const [error, setError] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const API_URL = "http://localhost:8000/api/auth";

  useEffect(() => {
      if (localStorage.getItem("access_token")) {
          navigate("/dashboard");
      }
  }, []);

  const doLogin = () => {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    fetch(API_URL + "/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: params,
      redirect: "follow",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Invalid credentials");
        }
        return response.json();
      })
      .then((data) => {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        localStorage.setItem("token_type", data.token_type);
        navigate("/dashboard"); // 🚀 Redirect here
      })
      .catch((error) => setError(error.message));
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">Login</h1>
        <p className="login-subtitle">
          Use your username and password to access the system.
        </p>
        <input
          type="text"
          placeholder="Username"
          className="login-input"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          className="login-input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="login-button" onClick={doLogin}>
          Login
        </button>
        {error && <p className="login-error">{error}</p>}
      </div>
    </div>
  );
}

export default Login;
