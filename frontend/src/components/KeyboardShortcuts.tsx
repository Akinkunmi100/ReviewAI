import React, { useEffect } from "react";
import { Keyboard } from "lucide-react";

interface Shortcut {
  key: string;
  description: string;
  action: () => void;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
}

interface Props {
  shortcuts: Shortcut[];
  showHelp?: boolean;
}

const KeyboardShortcuts: React.FC<Props> = ({ shortcuts, showHelp = false }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      shortcuts.forEach(shortcut => {
        const ctrlMatch = shortcut.ctrl ? e.ctrlKey || e.metaKey : !e.ctrlKey && !e.metaKey;
        const shiftMatch = shortcut.shift ? e.shiftKey : !e.shiftKey;
        const altMatch = shortcut.alt ? e.altKey : !e.altKey;
        
        if (
          e.key.toLowerCase() === shortcut.key.toLowerCase() &&
          ctrlMatch &&
          shiftMatch &&
          altMatch
        ) {
          e.preventDefault();
          shortcut.action();
        }
      });
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts]);

  if (!showHelp) return null;

  return (
    <div style={{
      position: 'fixed',
      bottom: 'var(--space-xl)',
      left: 'var(--space-xl)',
      background: 'var(--glass-bg)',
      backdropFilter: 'var(--backdrop-blur)',
      border: '1px solid var(--glass-border)',
      borderRadius: 'var(--radius-xl)',
      padding: 'var(--space-lg)',
      boxShadow: 'var(--shadow-xl)',
      maxWidth: '300px',
      zIndex: 100,
      animation: 'slideInUp 0.3s ease-out'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-sm)',
        marginBottom: 'var(--space-md)',
        color: 'var(--color-text-main)',
        fontWeight: 600
      }}>
        <Keyboard size={18} />
        <span>Keyboard Shortcuts</span>
      </div>
      
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--space-sm)'
      }}>
        {shortcuts.map((shortcut, i) => (
          <div key={i} style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '0.875rem'
          }}>
            <span style={{ color: 'var(--color-text-secondary)' }}>
              {shortcut.description}
            </span>
            <kbd style={{
              padding: '2px 8px',
              background: 'var(--color-surface)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.8125rem',
              fontFamily: 'monospace',
              color: 'var(--color-text-main)'
            }}>
              {shortcut.ctrl && 'Ctrl+'}
              {shortcut.shift && 'Shift+'}
              {shortcut.alt && 'Alt+'}
              {shortcut.key.toUpperCase()}
            </kbd>
          </div>
        ))}
      </div>
    </div>
  );
};

export default KeyboardShortcuts;
