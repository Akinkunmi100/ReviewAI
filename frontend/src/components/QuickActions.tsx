import React from "react";
import { TrendingUp, Smartphone, Laptop, Tv, Watch, Headphones } from "lucide-react";

interface Props {
  onSearch: (term: string) => void;
}

const QuickActions: React.FC<Props> = ({ onSearch }) => {
  const quickSearches = [
    { label: "Smartphones", icon: Smartphone, query: "iPhone 15 Pro" },
    { label: "Laptops", icon: Laptop, query: "MacBook Pro M3" },
    { label: "TVs", icon: Tv, query: "Samsung 65 inch Smart TV" },
    { label: "Smartwatches", icon: Watch, query: "Apple Watch Series 9" },
    { label: "Audio", icon: Headphones, query: "Sony WH-1000XM5" }
  ];

  return (
    <div style={{
      marginBottom: 'var(--space-xl)'
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-sm)',
        marginBottom: 'var(--space-md)',
        color: 'var(--color-text-subtle)',
        fontSize: '0.875rem',
        fontWeight: 500
      }}>
        <TrendingUp size={16} />
        <span>Popular Categories</span>
      </div>
      
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: 'var(--space-sm)'
      }}>
        {quickSearches.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.label}
              onClick={() => onSearch(item.query)}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 'var(--space-xs)',
                padding: 'var(--space-sm) var(--space-md)',
                background: 'var(--glass-bg)',
                backdropFilter: 'var(--backdrop-blur)',
                border: '1px solid var(--glass-border)',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: 'var(--color-text-secondary)',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: 'var(--shadow-sm)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'var(--color-primary-soft)';
                e.currentTarget.style.borderColor = 'var(--color-primary)';
                e.currentTarget.style.color = 'var(--color-primary)';
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'var(--glass-bg)';
                e.currentTarget.style.borderColor = 'var(--glass-border)';
                e.currentTarget.style.color = 'var(--color-text-secondary)';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
              }}
            >
              <Icon size={16} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default QuickActions;
