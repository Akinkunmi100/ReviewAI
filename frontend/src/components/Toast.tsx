import React, { useEffect } from "react";
import { CheckCircle, AlertCircle, Info, X } from "lucide-react";

interface Props {
  message: string;
  type?: "success" | "error" | "info";
  onClose: () => void;
  duration?: number;
}

const Toast: React.FC<Props> = ({ message, type = "info", onClose, duration = 4000 }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const configs = {
    success: {
      icon: CheckCircle,
      color: 'var(--color-success)',
      bg: 'var(--color-success-soft)',
      border: 'var(--color-success)'
    },
    error: {
      icon: AlertCircle,
      color: 'var(--color-danger)',
      bg: 'var(--color-danger-soft)',
      border: 'var(--color-danger)'
    },
    info: {
      icon: Info,
      color: 'var(--color-primary)',
      bg: 'var(--color-primary-soft)',
      border: 'var(--color-primary)'
    }
  };

  const config = configs[type];
  const Icon = config.icon;

  return (
    <div style={{
      position: 'fixed',
      bottom: 'var(--space-xl)',
      right: 'var(--space-xl)',
      zIndex: 1000,
      background: config.bg,
      border: `2px solid ${config.border}`,
      borderRadius: 'var(--radius-lg)',
      padding: 'var(--space-md) var(--space-lg)',
      display: 'flex',
      alignItems: 'center',
      gap: 'var(--space-md)',
      boxShadow: 'var(--shadow-xl)',
      backdropFilter: 'var(--backdrop-blur)',
      minWidth: '300px',
      maxWidth: '500px',
      animation: 'slideInUp 0.3s ease-out'
    }}>
      <Icon size={24} style={{ color: config.color, flexShrink: 0 }} />
      <p style={{
        flex: 1,
        margin: 0,
        fontSize: '0.9375rem',
        fontWeight: 500,
        color: 'var(--color-text-main)'
      }}>
        {message}
      </p>
      <button
        onClick={onClose}
        style={{
          background: 'transparent',
          border: 'none',
          padding: 'var(--space-xs)',
          cursor: 'pointer',
          color: 'var(--color-text-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderRadius: 'var(--radius-sm)',
          transition: 'all 0.2s ease',
          minWidth: 'auto',
          boxShadow: 'none'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'rgba(0, 0, 0, 0.1)';
          e.currentTarget.style.color = 'var(--color-text-main)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.color = 'var(--color-text-subtle)';
        }}
      >
        <X size={18} />
      </button>
    </div>
  );
};

export default Toast;
