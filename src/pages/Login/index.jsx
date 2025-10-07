import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // 👈 para redirigir
import "./Login.css";
import logo from "../../assets/logo.png";

const Login = () => {
  const navigate = useNavigate();

  const usuario = {
    user: "admin@example.com",
    password: "123456",
  };

  const [formData, setFormData] = useState({
    user: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (formData.user === usuario.user && formData.password === usuario.password) {
      navigate("/home"); // 👈 redirige con React Router
    } else {
      alert("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div className="login-body">
      <div className="login-form">
        <img src={logo} alt="Logo" />
        <form id="form-login" onSubmit={handleSubmit}>
          <h5 className="text-center mb-3">INICIO DE SESIÓN</h5>

          <div className="form-floating mb-1">
            <input
              type="email"
              className="form-control"
              id="user"
              placeholder="name@example.com"
              value={formData.user}
              onChange={handleChange}
              required
            />
            <label htmlFor="user">Usuario</label>
          </div>

          <div className="form-floating mb-3">
            <input
              type="password"
              className="form-control"
              id="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <label htmlFor="password">Contraseña</label>
          </div>

          <button type="submit" className="btn btn-dark">
            Iniciar sesión
          </button>
        </form>
      </div>
    </div>
  );
};

export { Login };
