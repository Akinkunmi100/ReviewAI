import React from "react";
import { Loader2 } from "lucide-react";

interface Props {
  message?: string;
  size?: "sm" | "md" | "lg";
}

const LoadingSpinner: React.FC<Props> = ({ message = "Analyzing product...", size = "md" }) => {
  const sizes = {
    sm: { icon: 20, text: '0.875rem' },
    md: { icon: 32, text: '1rem' },
    lg: { icon: 48, text: '1.125rem' }
  };

  const sizeConfig = sizes[size];

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 'var(--space-2xl)',
      gap: 'var(--space-lg)'
    }}>
      <div style={{
        animation: 'spin 1s linear infinite',
        color: 'var(--color-primary)'
      }}>
        <Loader2 size={sizeConfig.icon} strokeWidth={2.5} />
      </div>
      
      {message && (
        <div style={{
          textAlign: 'center'
        }}>
          <p style={{
            fontSize: sizeConfig.text,
            fontWeight: 600,
            color: 'var(--color-text-main)',
            marginBottom: 'var(--space-xs)'
          }}>
            {message}
          </p>
          <p style={{
            fontSize: '0.875rem',
            color: 'var(--color-text-subtle)'
          }}>
            This may take a few seconds...
          </p>
        </div>
      )}
    </div>
  );
};

export default LoadingSpinner;
