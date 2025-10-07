import React from "react";
import { NavBar } from '../../components/NavBar';
import { PrimaryForm } from "../../components/PrimaryForm";
import "./Home.css";

const Home = () => {
  return (
    <div>
      <NavBar />
      <PrimaryForm />
    </div>
  );
};

export { Home };