import React, { useState, useEffect } from 'react';
import { HashRouter, Routes, Route, useLocation } from 'react-router-dom';
import { Login } from '../pages/Login';
import { Home } from '../pages/Home';
import { Modal } from '../components/Modal';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalContent, setModalContent] = useState(null);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 790);

  const showModal = (content) => {
    setModalContent(content);
    setIsModalVisible(true);
  };

  const hideModal = () => {
    setIsModalVisible(false);
    setModalContent(null);
  };

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="App">
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path='/home' element={<Home showModal={showModal} />} />
      </Routes>
      <Modal isVisible={isModalVisible} hideModal={hideModal} content={modalContent} />
    </div>
  );
}

function AppWithRouter() {
  return (
    <HashRouter>
      <App />
    </HashRouter>
  );
}

export { AppWithRouter as App };