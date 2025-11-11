import type { ReactNode } from "react";
import { useFontSize } from "./FontSizeContext";
import "../src/index.css";

export default function Layout({ children }: { children: ReactNode }) {
  const { isLarge } = useFontSize();
  
  return (
    <div className={`main-container ${isLarge ? "text-large" : ""}`}>
      {children}
    </div>
  );
}