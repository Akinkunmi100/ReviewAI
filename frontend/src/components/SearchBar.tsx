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

  // Diverse placeholders to show universal capability
  const PLACEHOLDERS = [
    "Iphone 15, Samsung S23 Ultra",  // Comparison example
    "Nike Air Max 90",
    "Sony WH-1000XM5",
    "Dyson V15 Detect",
    "MacBook Pro M3",
    "Levi's 501 Jeans",
    "PlayStation 5",
    "LG C3 OLED TV",
    "Canon EOS R5",
    "Hp and Acer laptop bag" // Comparison example
  ];

  const [placeholderIndex, setPlaceholderIndex] = useState(0);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholderIndex((prev) => (prev + 1) % PLACEHOLDERS.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const validationError = validateInput(value);
    if (validationError) {
      setError(validationError);
      return;
    }

    onAnalyze(value.trim());
    setValue(""); // Clear search input after successful search
  };

  return (
    <>
      <form className="search-bar" onSubmit={handleSubmit}>
        <Search size={20} style={{ color: 'var(--color-text-subtle)', flexShrink: 0 }} />
        <input
          value={value}
          placeholder={`Search or Compare (e.g., ${PLACEHOLDERS[placeholderIndex]})`}
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
