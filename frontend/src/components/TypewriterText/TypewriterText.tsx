import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { includesSafe } from "../../utils/safeHelpers";
import './TypewriterText.css';

// Speed presets (characters per second approximation)
export type SpeedPreset = 'slow' | 'normal' | 'fast' | 'instant';

const SPEED_PRESETS: Record<SpeedPreset, number> = {
  slow: 80,      // ~12 chars/sec
  normal: 30,    // ~33 chars/sec
  fast: 12,      // ~83 chars/sec
  instant: 0,    // No animation
};

interface TypewriterTextProps {
  text: string;
  /** Speed in ms per character, or use a preset: 'slow' | 'normal' | 'fast' | 'instant' */
  speed?: number | SpeedPreset;
  delay?: number;
  className?: string;
  cursor?: boolean;
  highlightText?: string;
  onComplete?: () => void;
  /** If true, types word-by-word instead of character-by-character (faster for long text) */
  wordMode?: boolean;
  /** Skip animation and show full text immediately */
  skipAnimation?: boolean;
}

const TypewriterText: React.FC<TypewriterTextProps> = ({
  text,
  speed = 'fast',
  delay = 0,
  className = '',
  cursor = true,
  highlightText,
  onComplete,
  wordMode = false,
  skipAnimation = false,
}) => {
  const [displayText, setDisplayText] = useState('');
  const [isTypingComplete, setIsTypingComplete] = useState(false);

  // Resolve speed preset to actual ms value
  const resolvedSpeed = useMemo(() => {
    if (typeof speed === 'string') {
      return SPEED_PRESETS[speed] ?? SPEED_PRESETS.fast;
    }
    return speed;
  }, [speed]);

  // Split text into tokens (characters or words)
  const tokens = useMemo(() => {
    if (wordMode) {
      // Split into words while preserving whitespace
      const parts: string[] = [];
      let current = '';
      for (const char of text) {
        if (char === ' ' || char === '\n') {
          if (current) parts.push(current);
          parts.push(char);
          current = '';
        } else {
          current += char;
        }
      }
      if (current) parts.push(current);
      return parts;
    }
    return text.split('');
  }, [text, wordMode]);

  // Handle instant/skip modes
  useEffect(() => {
    if (skipAnimation || resolvedSpeed === 0) {
      setDisplayText(text);
      setIsTypingComplete(true);
      onComplete?.();
    }
  }, [skipAnimation, resolvedSpeed, text, onComplete]);

  // Main typing effect
  useEffect(() => {
    if (skipAnimation || resolvedSpeed === 0) return;

    let currentIndex = 0;
    let timeoutId: ReturnType<typeof setTimeout>;
    let isCancelled = false;

    const typeNext = () => {
      if (isCancelled) return;

      if (currentIndex < tokens.length) {
        // Build display text from tokens
        const newText = tokens.slice(0, currentIndex + 1).join('');
        setDisplayText(newText);
        currentIndex++;

        // Add slight natural variance (±20%) for more human feel
        const variance = resolvedSpeed * 0.2 * (Math.random() - 0.5);
        const nextDelay = Math.max(5, resolvedSpeed + variance);

        timeoutId = setTimeout(typeNext, nextDelay);
      } else {
        setIsTypingComplete(true);
        onComplete?.();
      }
    };

    // Initial delay before starting
    const startTimeout = setTimeout(() => {
      typeNext();
    }, delay);

    return () => {
      isCancelled = true;
      clearTimeout(startTimeout);
      clearTimeout(timeoutId);
    };
  }, [tokens, resolvedSpeed, delay, onComplete, skipAnimation]);

  // Reset state when text changes
  useEffect(() => {
    if (!skipAnimation && resolvedSpeed !== 0) {
      setDisplayText('');
      setIsTypingComplete(false);
    }
  }, [text, skipAnimation, resolvedSpeed]);

  // Render with optional highlight
  const renderContent = useCallback(() => {
    if (!highlightText || !includesSafe(displayText, highlightText)) {
      return displayText;
    }

    const index = displayText.indexOf(highlightText);
    if (index === -1) return displayText;

    return (
      <>
        {displayText.slice(0, index)}
        <span className="highlight">{highlightText}</span>
        {displayText.slice(index + highlightText.length)}
      </>
    );
  }, [displayText, highlightText]);

  return (
    <span className={`typewriter-text ${className}`}>
      {renderContent()}
      {cursor && !isTypingComplete && <span className="typewriter-cursor" />}
    </span>
  );
};

export default TypewriterText;
