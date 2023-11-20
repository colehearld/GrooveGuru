import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './roundbutton.css';
import './styles.css';
import { useLikesDislikes } from './LikesDislikesContext'; 

export function HomePage() {
  const [currentSong, setCurrentSong] = useState<SongData | null>(null);

  interface SongData {
    photo: string;
    name: string;
    song_name: string;
  }

  // Destructuring values from the LikesDislikesContext
  const { likedSongs, dislikedSongs, likeSong, dislikeSong } = useLikesDislikes();
  
  // State variables
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isZoomed, setIsZoomed] = useState(false);
  
  // Function for programmatic navigation
  const navigate = useNavigate();

  // Opens the modal
  const openModal = () => {
    setIsModalOpen(true);
  };

  // Closes the modal and resets zoom
  const closeModal = () => {
    setIsModalOpen(false);
    setIsZoomed(false);
  };

  // Handles the end of the zoom transition
  const handleTransitionEnd = () => {
    if (isZoomed) {
      // If zoom is complete, open the popup
      openModal();
    }
  };

  const handleFindGrooveClick = () => {
    // Make an HTTP request to your backend API
    fetch('http://127.0.0.1:5000')
      .then((response: Response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Check for the presence of 'message'
        if ('message' in data) {
          console.log('Message from Flask:', data.message);
        }
  
        // Handle the data received from the backend
        console.log('Data from Flask:', data);
        setCurrentSong(data);
  
        // Initiate zoom after receiving data
        setIsZoomed(true);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };
  

  const backgroundStyles: React.CSSProperties = {
    backgroundColor: 'transparent',
    backgroundImage: 'radial-gradient(circle at center, #ff8a00, #ff4377, #da1b60, #9d1be4, #2f7be7)',
    backgroundSize: '100% 100%',
    backgroundPosition: '50% 50%',
    animation: 'pulseBackground 2s infinite',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    transition: 'transform 1.25s',
    transform: isZoomed ? 'scale(4)' : 'scale(1)',
  };

  // Styles for the user profile button
  const userProfileStyles: React.CSSProperties = {
    position: 'absolute',
    top: '20px',
    left: '20px',
    fontSize: '1.2em',
  };

  // Styles for the "Groove Guru" headings
  const grooveGuruStyles = {
    color: 'Yellow',
    textShadow: '4px 4px 2px rgba(0, 0, 0, 0.8)',
    fontSize: '4em',
    marginBottom: '20px',
    animation: 'dance 1s infinite',
    transform: 'translate(0)',
  };

  // Handles the click on the "User Profile" button
  const handleButtonClick = () => {
    navigate('/user');
  };

  // Handles liking a song, calls the corresponding context function, and closes the modal
  const handleLikeSong = (song: string) => {
    likeSong(song);
    closeModal();
  };

  // Handles disliking a song, calls the corresponding context function, and closes the modal
  const handleDislikeSong = (song: string) => {
    dislikeSong(song);
    closeModal();
  };

  return (
    <div style={backgroundStyles} onTransitionEnd={handleTransitionEnd}>
      <button
        className="round-button user-profile-button"
        style={userProfileStyles}
        onClick={handleButtonClick}
      >
        User Profile
      </button>
      <h1 style={{ ...grooveGuruStyles, color: 'purple' }}>Groove</h1>
      <h1 style={{ ...grooveGuruStyles, color: 'yellow' }}>Guru</h1>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          flex: 1,
          justifyContent: 'center',
        }}
      >
        <button
          onClick={handleFindGrooveClick}
          className="round-button"
          style={{ fontSize: '4em', padding: '20px', width: '650px', height: '650px' }}
        >
          FIND ME THE GROOVE
        </button>
      </div>
      {isModalOpen && currentSong && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <div
            style={{
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '10px',
              boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.5)',
            }}
          >
            <h2>Groove Found</h2>
            <img
              src={currentSong.photo}
              alt="Groove Image"
              style={{
                maxWidth: '100%',
                maxHeight: '200px',
                marginBottom: '10px',
              }}
            />
            <p>{currentSong.name}: {currentSong.song_name}</p>
            <button onClick={() => handleLikeSong(currentSong.song_name)}>Like</button>
            <button onClick={() => handleDislikeSong(currentSong.song_name)}>Dislike</button>
            <button onClick={closeModal}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}