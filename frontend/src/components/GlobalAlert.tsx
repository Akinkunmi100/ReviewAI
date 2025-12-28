import React from "react";

interface GlobalAlertProps {
  message: string | null;
  onClose?: () => void;
}

const GlobalAlert: React.FC<GlobalAlertProps> = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="global-alert" role="status" aria-live="polite">
      <span>{message}</span>
      {onClose && (
        <button type="button" onClick={onClose} className="global-alert-close">
          ×
        </button>
      )}
    </div>
  );
};

export default GlobalAlert;