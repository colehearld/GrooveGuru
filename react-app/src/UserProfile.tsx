import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './roundbutton.css';
import './UserBackStyles.css';
import { useLikesDislikes, SongData } from './LikesDislikesContext';

interface LikesDislikesPopupProps {
  items: SongData[];
  onRemoveItem: (item: SongData) => void;
}

const UserProfile: React.FC = () => {
  const { likedSongs, dislikedSongs, removeLikedSong, removeDislikedSong } = useLikesDislikes();

  const [showPopup, setShowPopup] = useState(false);
  const [showConfirmationPopup, setShowConfirmationPopup] = useState(false);
  const [popupText, setPopupText] = useState('');
  const [popupItems, setPopupItems] = useState<SongData[]>([]);
  const [itemToRemove, setItemToRemove] = useState<SongData | null>(null);

  const backgroundStyles: React.CSSProperties = {
    backgroundColor: 'transparent',
    backgroundImage:
      'repeating-linear-gradient(45deg, #ff8a00, #ff4377 250px, #da1b60 30px, #9d1be4 30px, #2f7be7 25px)',
    animation: 'gradientAnimation 5s linear infinite',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
  };

  const handleButtonClick = (text: string): void => {
    setPopupText(text);

    switch (text) {
      case 'Likes':
        setPopupItems(likedSongs);
        break;
      case 'Dislikes':
        setPopupItems(dislikedSongs);
        break;
      default:
        setPopupItems([]);
    }
    setShowPopup(true);
  };

  const removeItem = (item: SongData): void => {
    setItemToRemove(item);
    setShowConfirmationPopup(true);
  };

  const closePopup = (): void => {
    setShowPopup(false);
  };

  const handleConfirmRemove = (): void => {
    if (itemToRemove) {
      // Determine whether it's a liked or disliked song and call the appropriate context function
      if (likedSongs.includes(itemToRemove)) {
        removeLikedSong(itemToRemove);
      } else if (dislikedSongs.includes(itemToRemove)) {
        removeDislikedSong(itemToRemove);
      }
      // Close all popups
      closeAllPopups();
    }
  };

  const handleCancelRemove = (): void => {
    setShowConfirmationPopup(false);
  };

  const closeAllPopups = (): void => {
    setShowPopup(false);
    setShowConfirmationPopup(false);
  };

  return (
    <div className="gradient-animation" style={{ ...backgroundStyles }}>
      <h1 className="dvd-logo-effect" style={{ color: '#da1b77' }}>User</h1>
      <h1 className="dvd-logo-effect_1" style={{ color: 'orange' }}>Profile</h1>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button
          className="round-button dvd-bounce"
          style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            width: '345px',
            height: '345px',
            fontSize: '3em',
          }}
          onClick={() => handleButtonClick('Likes')}
        >
          Likes
        </button>
        <button
          className="round-button dvd-bounce"
          style={{
            position: 'fixed',
            bottom: '20px',
            left: '20px',
            width: '345px',
            height: '345px',
            fontSize: '3em',
          }}
          onClick={() => handleButtonClick('Dislikes')}
        >
          Dislikes
        </button>
        <Link to="/home" 
        style={{ textDecoration: 'none', 
        position: 'fixed', 
        top: '20px', 
        left: '50%', 
        transform: 'translateX(-50%)' }}>
          <button
            className="round-button"
            style={{
              width: '345px',
              height: '345px',
              fontSize: '3em',
            }}
          >
            Back to Homepage
          </button>
        </Link>
      </div>

      <div className={`big-popup ${showPopup ? 'show' : ''}`}>
        <h2>{popupText}</h2>
        {(popupText === 'Likes' || popupText === 'Dislikes') && (
          <LikesDislikesPopup items={popupItems} onRemoveItem={removeItem} />
        )}
        <button className="close-button" onClick={closePopup}>
          Close
        </button>
      </div>

      {showConfirmationPopup && (
  <div className="popup">
    <div className="big-popup show">
      <h2>Are You Sure You Want to Remove:</h2>
      <div className="song-details">
        {itemToRemove && (
          <>
            {itemToRemove.photo && (
              <div>
                <img
                  src={itemToRemove.photo}
                  alt={`Cover for ${itemToRemove.song_name}`}
                  style={{ maxWidth: '100px', maxHeight: '100px', marginBottom: '10px' }}
                />
              </div>
            )}
            <div>
              <strong>Song:</strong> {itemToRemove.song_name}
            </div>
            <div>
              <strong>Artist(s):</strong> {itemToRemove.name}
            </div>
            <div>
              <strong>Date:</strong> {itemToRemove.date}
            </div>
            <div>
              <strong>Link:</strong> {itemToRemove.link}
            </div>
          </>
        )}
      </div>
      <div className="popup-buttons">
        <button onClick={() => handleConfirmRemove()}>Yes</button>
        <button onClick={handleCancelRemove}>Cancel</button>
      </div>
    </div>
  </div>
)}
    </div>
  );
};


const LikesDislikesPopup: React.FC<LikesDislikesPopupProps> = ({ items, onRemoveItem }) => (
  <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
    <ul>
      {items.map((item, index) => (
        <li key={index}>
          <div>
            <strong>Song:</strong> {item.song_name}
          </div>
          {item.photo && (
            <div>
              <img
                src={item.photo}
                alt={`Cover for ${item.song_name}`}
                style={{ maxWidth: '100px', maxHeight: '100px', marginBottom: '10px' }}
              />
            </div>
          )}
          <div>
            <strong>Artist(s):</strong> {item.name}
          </div>
          <div>
            <strong>Date:</strong> {item.date}
          </div>
          <div>
            <strong>Link:</strong> {item.link}
          </div>
          <button onClick={() => onRemoveItem(item)}>Remove</button>
        </li>
      ))}
    </ul>
  </div>
);

export default UserProfile;
