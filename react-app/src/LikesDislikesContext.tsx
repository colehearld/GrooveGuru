import React, { createContext, useContext, useState, ReactNode } from 'react';

// Define the type for the context
interface LikesDislikesContextType {
  likedSongs: string[]; 
  dislikedSongs: string[]; 
  likeSong: (song: string) => void;
  dislikeSong: (song: string) => void;
  removeLikedSong: (song: string) => void; 
  removeDislikedSong: (song: string) => void;
}

const LikesDislikesContext = createContext<LikesDislikesContextType | undefined>(undefined);

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
  const [likedSongs, setLikedSongs] = useState<string[]>([]);
  const [dislikedSongs, setDislikedSongs] = useState<string[]>([]);

  const likeSong = (song: string) => {
    setLikedSongs([...likedSongs, song]);
  };

  const dislikeSong = (song: string) => {
    setDislikedSongs([...dislikedSongs, song]);
  };

  const removeLikedSong = (song: string) => {
    setLikedSongs(likedSongs.filter((likedSong) => likedSong !== song));
  };

  const removeDislikedSong = (song: string) => {
    setDislikedSongs(dislikedSongs.filter((dislikedSong) => dislikedSong !== song));
  };

  // Provide the context value with the appropriate types
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
      {children}
    </LikesDislikesContext.Provider>
  );
};
