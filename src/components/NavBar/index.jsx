import React from "react";
import { Link, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import logo from "../../assets/logo.png";
import { ImExit } from "react-icons/im";
import "./NavBar.css";

const NavBar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    Swal.fire({
      title: "¿Estás seguro?",
      text: "Se cerrará tu sesión actual.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, cerrar sesión",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        // Limpias sesión (token, storage, etc.)
        localStorage.removeItem("authToken");

        // Aviso de éxito
        Swal.fire({
          title: "Sesión cerrada",
          text: "Has cerrado sesión correctamente.",
          icon: "success",
          timer: 2000,
          showConfirmButton: false,
        });

        // Redirigir al login (con pequeño delay para mostrar el alert)
        setTimeout(() => {
          navigate("/");
        }, 2000);
      }
    });
  };

  return (
    <div className="navBar d-flex justify-content-around align-items-center px-3">
      {/* Logo */}
      <div className="navBar__logo aiex-logo-navbar">
        <Link to="/home" style={{ textDecoration: "none" }}>
          <img src={logo} alt="logo" />
        </Link>
      </div>

      {/* Botón de logout */}
      <button
        className="btnForm gap-2 d-flex align-items-center btn btn-link text-decoration-none text-dark"
        onClick={handleLogout}
      >
        <span>Cerrar Sesión</span>
        <ImExit />
      </button>
    </div>
  );
};

export { NavBar };
