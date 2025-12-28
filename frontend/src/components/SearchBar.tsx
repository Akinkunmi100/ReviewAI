import React, { useState } from "react";
import { Search, Sparkles } from "lucide-react";

interface Props {
  onAnalyze: (name: string) => void;
  dataMode: "web" | "ai" | "hybrid";
  setDataMode: (val: "web" | "ai" | "hybrid") => void;
}

const SearchBar: React.FC<Props> = ({ onAnalyze, dataMode, setDataMode }) => {
  const [value, setValue] = useState("");
  const [error, setError] = useState<string | null>(null);

  const validateInput = (input: string): string | null => {
    const trimmed = input.trim();
    if (!trimmed) {
      return "Please enter a product name";
    }
    if (trimmed.length > 200) {
      return "Product name must be 200 characters or less";
    }
    // Check for potentially dangerous characters
    if (/[<>"'\\\/]/.test(trimmed)) {
      return "Product name contains invalid characters";
    }
    return null;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    
    const validationError = validateInput(value);
    if (validationError) {
      setError(validationError);
      return;
    }
    
    onAnalyze(value.trim());
  };

  return (
    <>
      <form className="search-bar" onSubmit={handleSubmit}>
        <Search size={20} style={{ color: 'var(--color-text-subtle)', flexShrink: 0 }} />
        <input
          value={value}
          placeholder="Search for any product..."
          onChange={(e) => {
            setValue(e.target.value);
            if (error) setError(null); // Clear error on input change
          }}
          onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
          aria-invalid={!!error}
        />
      <div className="search-options">
        <label>
          <input
            type="radio"
            checked={dataMode === "web"}
            onChange={() => setDataMode("web")}
          />
          <span>Web search</span>
        </label>
        <label>
          <input
            type="radio"
            checked={dataMode === "hybrid"}
            onChange={() => setDataMode("hybrid")}
          />
          <span>Hybrid (web + AI)</span>
        </label>
        <label>
          <input
            type="radio"
            checked={dataMode === "ai"}
            onChange={() => setDataMode("ai")}
          />
          <span>AI knowledge</span>
        </label>
      </div>
      <button type="submit" disabled={!value.trim()}>
        <Sparkles size={18} />
        Analyze
      </button>
    </form>
    {error && (
      <div style={{ color: 'var(--color-error, #e74c3c)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
        {error}
      </div>
    )}
    </>
  );
};

export default SearchBar;
