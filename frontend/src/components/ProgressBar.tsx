import React from "react";

interface Props {
  progress: number; // 0-100
  message?: string;
  showPercentage?: boolean;
}

const ProgressBar: React.FC<Props> = ({ progress, message, showPercentage = true }) => {
  return (
    <div style={{
      width: '100%',
      padding: 'var(--space-lg)',
      background: 'var(--glass-bg)',
      backdropFilter: 'var(--backdrop-blur)',
      border: '1px solid var(--glass-border)',
      borderRadius: 'var(--radius-xl)',
      boxShadow: 'var(--shadow-md)'
    }}>
      {message && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 'var(--space-md)'
        }}>
          <p style={{
            margin: 0,
            fontSize: '0.9375rem',
            fontWeight: 600,
            color: 'var(--color-text-main)'
          }}>
            {message}
          </p>
          {showPercentage && (
            <span style={{
              fontSize: '0.875rem',
              fontWeight: 600,
              color: 'var(--color-primary)'
            }}>
              {Math.round(progress)}%
            </span>
          )}
        </div>
      )}
      
      <div style={{
        width: '100%',
        height: '8px',
        background: 'var(--color-primary-soft)',
        borderRadius: 'var(--radius-full)',
        overflow: 'hidden',
        position: 'relative'
      }}>
        <div style={{
          width: `${progress}%`,
          height: '100%',
          background: 'var(--color-primary-gradient-vivid)',
          borderRadius: 'var(--radius-full)',
          transition: 'width 0.5s ease',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent)',
            animation: 'barShimmer 2s infinite'
          }} />
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;
