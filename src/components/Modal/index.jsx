// components/Modal.js
import React from 'react';
import ReactDOM from 'react-dom';
import './Modal.css';

const Modal = ({ isVisible, hideModal, content }) => {
  if (!isVisible) return null;

  return ReactDOM.createPortal(
    <div className="modal-overlay">
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-cont">
          <button className="modal-close" onClick={hideModal}>X</button>
          {content}
        </div>
      </div>
    </div>,
    document.getElementById('modal')
  );
};

export { Modal };