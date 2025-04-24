import React from 'react';

interface ActionButtonProps {
  label: string;
  onClick: () => void;
  className?: string;
}

export const ActionButton: React.FC<ActionButtonProps> = ({ label, onClick, className }) => {
  return (
    <button
      onClick={onClick}
      className={`bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition ${className}`}
    >
      {label}
    </button>
  );
};
