import React from 'react';

interface BigCircularPopupProps {
  onClose: () => void;
}

const BigCircularPopup: React.FC<BigCircularPopupProps> = ({ onClose }) => {
  return (
    <div className="big-circular-popup">
      <p>This is the big circular popup content.</p>
      <button className="close-button" onClick={onClose}>
        Close
      </button>
    </div>
  );
}

export default BigCircularPopup;
