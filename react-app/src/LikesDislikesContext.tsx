import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';

// Define the type for the context
export interface LikesDislikesContextType {
  likedSongs: SongData[]; 
  dislikedSongs: SongData[]; 
  likeSong: (song: SongData) => void;
  dislikeSong: (song: SongData) => void;
  removeLikedSong: (song: SongData) => void; 
  removeDislikedSong: (song: SongData) => void;
}

export interface SongData {
  photo: string;
  name: string;
  song_name: string;
  link: string;
  date: string;
}

export const LikesDislikesContext = createContext<LikesDislikesContextType | undefined>(undefined);

export const useLikesDislikes = (): LikesDislikesContextType => {
  const context = useContext(LikesDislikesContext);

  if (!context) {
    throw new Error('useLikesDislikes must be used within a LikesDislikesProvider');
  }

  return context;
};

interface LikesDislikesProviderProps {
  children: ReactNode;
}

export const LikesDislikesProvider: React.FC<LikesDislikesProviderProps> = ({ children }) => {
  const [likedSongs, setLikedSongs] = useState<SongData[]>([]);
  const [dislikedSongs, setDislikedSongs] = useState<SongData[]>([]);

  useEffect(() => {
    updateBackend(); // Update backend when likedSongs or dislikedSongs change
  }, [likedSongs, dislikedSongs]);

  const likeSong = (song: SongData) => {
    setLikedSongs([...likedSongs, song]);
  };

  const dislikeSong = (song: SongData) => {
    setDislikedSongs([...dislikedSongs, song]);
  };

  const removeLikedSong = (song: SongData) => {
    setLikedSongs((prevLikedSongs) => {
      const index = prevLikedSongs.findIndex((s) => s.song_name === song.song_name);

      if (index !== -1) {
        prevLikedSongs.splice(index, 1);
        return [...prevLikedSongs];
      }

      return prevLikedSongs;
    });
  };

  const removeDislikedSong = (song: SongData) => {
    setDislikedSongs((prevDislikedSongs) => {
      const index = prevDislikedSongs.findIndex((s) => s.song_name === song.song_name);

      if (index !== -1) {
        prevDislikedSongs.splice(index, 1);
        return [...prevDislikedSongs];
      }

      return prevDislikedSongs;
    });
  };

  const updateBackend = () => {
    const backendEndpoint = 'http://127.0.0.1:5000/api/updateLikesDislikes';

    const requestBody = {
      likedSongs,
      dislikedSongs,
    };

    // Make a POST request to update the backend
    fetch(backendEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        // Handle success response from the backend 
        console.log('Backend updated successfully:', data);
      })
      .catch((error) => {
        console.error('Error updating backend:', error);
      });
  };

  const contextValue: LikesDislikesContextType = {
    likedSongs,
    dislikedSongs,
    likeSong,
    dislikeSong,
    removeLikedSong,
    removeDislikedSong,
  };

  return (
    <LikesDislikesContext.Provider value={contextValue}>
      {/* Include the new component */}
      <LikedDislikedSongsComponent />
      {children}
    </LikesDislikesContext.Provider>
  );
};

// New Component
const LikedDislikedSongsComponent: React.FC = () => {
  const { likedSongs, dislikedSongs } = useLikesDislikes();

  useEffect(() => {
    // Fetch liked and disliked songs from the backend when the component mounts
    fetchLikesDislikesFromBackend();
  }, []);

  const fetchLikesDislikesFromBackend = () => {
    // Make a GET request to the backend to fetch liked and disliked songs
    fetch('http://127.0.0.1:5000/api/updateLikesDislikes')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.likedSongs) {
          console.log('Liked Songs from Backend:', data.likedSongs);
        } else {
          console.log('No Liked Songs from Backend');
        }

        if (data.dislikedSongs) {
          console.log('Disliked Songs from Backend:', data.dislikedSongs);
        } else {
          console.log('No Disliked Songs from Backend');
        }
      })
      .catch((error) => {
        console.error('Error fetching likes and dislikes from backend:', error);
      });
  };

  return (
    <div>
      <h2>Liked Songs</h2>
      {likedSongs.length > 0 ? (
        <ul>
          {likedSongs.map((song, index) => (
            <li key={index}>{song.song_name}</li>
          ))}
        </ul>
      ) : (
        <p>No liked songs.</p>
      )}

      <h2>Disliked Songs</h2>
      {dislikedSongs.length > 0 ? (
        <ul>
          {dislikedSongs.map((song, index) => (
            <li key={index}>{song.song_name}</li>
          ))}
        </ul>
      ) : (
        <p>No disliked songs.</p>
      )}
    </div>
  );
};

export default LikedDislikedSongsComponent;
