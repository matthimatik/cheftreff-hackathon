import React from 'react';
import { Button } from './components/ui/button';

interface ActionButtonProps {
  label: string;
  onClick: () => void;
  className?: string;
}

export const ActionButton: React.FC<ActionButtonProps> = ({ label, onClick, className }) => {
  return (
    <Button
      onClick={onClick}
      className={`w-full mt-4 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 ${className}`}
    >
      {label}
    </Button>
  );
};
