import { createContext, useContext, useState, useEffect } from 'react';

interface FontSizeContextType {
  isLarge: boolean;
  toggleSize: () => void;
}

const FontSizeContext = createContext<FontSizeContextType | undefined>(undefined);

export const FontSizeProvider = ({ children }: { children: React.ReactNode }) => {
  const [isLarge, setIsLarge] = useState(false);

  useEffect(() => {
    const savedSize = localStorage.getItem('textSize');
    if (savedSize) document.body.classList.toggle('text-large', savedSize === 'large');
  }, []);

  const toggleSize = () => {
    setIsLarge(!isLarge);
    document.body.classList.toggle('text-large');
    localStorage.setItem('textSize', !isLarge ? 'large' : 'normal');
  };

  return (
    <FontSizeContext.Provider value={{ isLarge, toggleSize }}>
      {children}
    </FontSizeContext.Provider>
  );
};

export const useFontSize = () => {
  const context = useContext(FontSizeContext);
  if (!context) {
    throw new Error("useFontSize must be used within a FontSizeProvider");
  }
  return context;
};