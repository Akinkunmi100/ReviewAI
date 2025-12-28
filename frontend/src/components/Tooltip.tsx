import React, { useState } from "react";
import { HelpCircle } from "lucide-react";

interface Props {
  content: string;
  children?: React.ReactNode;
}

const Tooltip: React.FC<Props> = ({ content, children }) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        style={{ 
          cursor: 'help',
          display: 'inline-flex',
          alignItems: 'center'
        }}
      >
        {children || <HelpCircle size={16} style={{ color: 'var(--color-text-subtle)' }} />}
      </div>
      
      {isVisible && (
        <div style={{
          position: 'absolute',
          bottom: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          marginBottom: 'var(--space-sm)',
          padding: 'var(--space-sm) var(--space-md)',
          background: 'var(--color-text-main)',
          color: 'var(--color-surface)',
          fontSize: '0.8125rem',
          borderRadius: 'var(--radius-md)',
          whiteSpace: 'nowrap',
          boxShadow: 'var(--shadow-lg)',
          zIndex: 100,
          animation: 'fadeInScale 0.2s ease-out',
          pointerEvents: 'none'
        }}>
          {content}
          <div style={{
            position: 'absolute',
            top: '100%',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 0,
            height: 0,
            borderLeft: '6px solid transparent',
            borderRight: '6px solid transparent',
            borderTop: '6px solid var(--color-text-main)'
          }} />
        </div>
      )}
    </div>
  );
};

export default Tooltip;
