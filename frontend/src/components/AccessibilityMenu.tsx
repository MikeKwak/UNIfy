import { useState } from "react";
import { useFontSize } from "../../fonts/FontSizeContext";

type AccessibilityMenuProps = {
  open: boolean;
  onClose: () => void;
};

export default function AccessibilityMenu({
  open,
  onClose,
}: AccessibilityMenuProps) {
  const { isLarge, toggleSize } = useFontSize();
  return (
    <div
      className={`fixed top-0 right-0 h-full w-80 bg-white shadow-lg border-l border-gray-200 transform transition-transform duration-300 z-50 ${
        open ? "translate-x-0" : "translate-x-full"
      }`}
    >
      {/* Close Menu */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 text-gray-600 hover:text-black"
      >
        ✕
      </button>

      <div className="p-6 mt-10 space-y-6">
        <h2 className="text-lg font-bold">Accessibility Settings</h2>
        <hr />

        {/* Text Size */}
        <div className="flex items-center justify-between">
          <span>{isLarge ? "Normal Text" : "Large Text"}</span>
          <button
            onClick={toggleSize}
            className={`relative inline-flex h-6 w-12 items-center rounded-full transition-colors ${
              isLarge ? "bg-lime-600" : "bg-gray-300"
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
          isLarge ? "translate-x-6" : "translate-x-1"
              }`}
            />
          </button>
        </div>
        <hr />

        {/* Dark Mode */}
        <Toggle label="Dark Mode" />
        <hr />

        {/* Dyslexia-Friendly Font */}
        <Toggle label="Dyslexia-Friendly Font" />
        <hr />

        {/* Keyboard Accessibility */}
        <Toggle label="Keyboard Accessibility" />
        <hr />
      </div>
    </div>
  );
}

function Toggle({ label }: { label: string }) {
  const [toggle, setToggle] = useState(false);
  return (
    <div className="flex items-center justify-between">
      <span>{label}</span>
      <button
        onClick={() => setToggle(!toggle)}
        className={`relative inline-flex h-6 w-12 items-center rounded-full transition-colors ${
          toggle ? "bg-lime-600" : "bg-gray-300"
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
            toggle ? "translate-x-6" : "translate-x-1"
          }`}
        />
      </button>
    </div>
  );
}
