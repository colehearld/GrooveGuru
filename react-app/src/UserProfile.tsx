import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './roundbutton.css';
import './UserBackStyles.css';
import { useLikesDislikes, SongData } from './LikesDislikesContext';

// Interface for representing user preferences for different music genres
interface MusicGenres {
  pop: boolean;
  rock: boolean;
  hipHop: boolean;
  jazz: boolean;
  classical: boolean;
  country: boolean;
  electronic: boolean;
  reggae: boolean;
}

// Update the type of items to be an array of SongData
interface LikesDislikesPopupProps {
  items: SongData[];
  onRemoveItem: (item: SongData) => void;
}

// UserProfile component
const UserProfile: React.FC = () => {
  // Destructuring values from the LikesDislikesContext
  const { likedSongs, dislikedSongs, removeLikedSong, removeDislikedSong } = useLikesDislikes();

  // State variables
  const [showPopup, setShowPopup] = useState(false);
  const [popupText, setPopupText] = useState('');
  const [popupItems, setPopupItems] = useState<SongData[]>([]);
  const [itemToRemove, setItemToRemove] = useState<SongData | null>(null);
  const [musicGenres, setMusicGenres] = useState<MusicGenres>({
    pop: false,
    rock: false,
    hipHop: false,
    jazz: false,
    classical: false,
    country: true,
    electronic: false,
    reggae: false,
  });

  // Animation-related state variables
  const [textPosition, setTextPosition] = useState({ top: 50, left: 50 });
  const [direction, setDirection] = useState({ top: 1, left: 1 });

  // Styles for the background gradient animation
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

  // Handles button clicks and sets up the popup based on the button clicked
  const handleButtonClick = (text: string): void => {
    setPopupText(text);

    switch (text) {
      case 'Preferences':
        setPopupItems(Object.keys(musicGenres).map((genre) => ({
          photo: '',
          name: '',
          song_name: genre,
          link: '',
          date: '',
        })));
        break;
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

  // Toggles the state of a music genre in the preferences popup
  const toggleGenre = (genre: keyof MusicGenres): void => {
    setMusicGenres({ ...musicGenres, [genre]: !musicGenres[genre] });
  };

  // Removes a liked or disliked item
  const removeItem = (item: SongData): void => {
    if (popupText === 'Likes') {
      removeLikedSong(item);
    } else if (popupText === 'Dislikes') {
      removeDislikedSong(item);
    }
  };

  // Closes the popup
  const closePopup = (): void => {
    setShowPopup(false);
  };

  return (
    <div className="gradient-animation" style={{ ...backgroundStyles }}>
      <h1 className="dvd-logo-effect">User Profile</h1>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button
          className="round-button dvd-bounce"
          style={{
            position: 'fixed',
            top: '20px',
            right: '20px',
            width: '300px',
            height: '300px',
            fontSize: '2em',
          }}
          onClick={() => handleButtonClick('Preferences')}
        >
          Preferences
        </button>
        <button
          className="round-button dvd-bounce"
          style={{
            position: 'fixed',
            top: '20px',
            left: '20px',
            width: '300px',
            height: '300px',
            fontSize: '2em',
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
            width: '300px',
            height: '300px',
            fontSize: '2em',
          }}
          onClick={() => handleButtonClick('Dislikes')}
        >
          Dislikes
        </button>
        <Link to="/home" style={{ textDecoration: 'none' }}>
          <button
            className="round-button"
            style={{
              position: 'fixed',
              bottom: '20px',
              right: '20px',
              width: '300px',
              height: '300px',
              fontSize: '2em',
            }}
          >
            Back to Homepage
          </button>
        </Link>
      </div>

      <div className={`big-popup ${showPopup ? 'show' : ''}`}>
        <h2>{popupText}</h2>
        {popupText === 'Preferences' && (
          <PreferencesPopup items={popupItems} genres={musicGenres} onToggleGenre={toggleGenre} />
        )}
        {(popupText === 'Likes' || popupText === 'Dislikes') && (
          <LikesDislikesPopup items={popupItems} onRemoveItem={removeItem} />
        )}
        <button className="close-button" onClick={closePopup}>
          Close
        </button>
      </div>
    </div>
  );
};

interface PreferencesPopupProps {
  items: SongData[];
  genres: MusicGenres;
  onToggleGenre: (genre: keyof MusicGenres) => void;
}

// Popup sliders
const PreferencesPopup: React.FC<PreferencesPopupProps> = ({ items, genres, onToggleGenre }) => (
  <ul>
    {items.map((genre) => (
      <li key={genre.song_name} style={{ marginBottom: '10px' }}>
        <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          {genre.song_name}
          <input
            type="range"
            min="0"
            max="1"
            step="1"
            value={genres[genre.song_name as keyof MusicGenres] ? 1 : 0}
            onChange={(e) => onToggleGenre(genre.song_name as keyof MusicGenres)}
            style={{ width: '50px' }}
          />
          <span>{genres[genre.song_name as keyof MusicGenres] ? 'Enabled' : 'Disabled'}</span>
        </label>
      </li>
    ))}
  </ul>
);

// Update the type of items to be an array of SongData
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
