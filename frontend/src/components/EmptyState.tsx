import React from "react";
import { Search, Sparkles, TrendingUp, ShoppingBag } from "lucide-react";

interface Props {
  type?: "initial" | "no-results" | "no-history" | "no-shortlist";
}

const EmptyState: React.FC<Props> = ({ type = "initial" }) => {
  const configs = {
    initial: {
      icon: Search,
      title: "Ready to find your perfect product?",
      description: "Search for any product to get AI-powered insights, price comparisons, and expert recommendations.",
      suggestions: [
        "Try searching for popular items like 'iPhone 15', 'Samsung TV', or 'HP Laptop'",
        "Get detailed pros & cons analysis",
        "Compare prices across Nigerian retailers",
        "See ratings and sentiment analysis"
      ]
    },
    "no-results": {
      icon: Search,
      title: "No results found",
      description: "We couldn't find any information about this product. Try a different search term or check the spelling.",
      suggestions: [
        "Use the product's full name or model number",
        "Try different variations of the product name",
        "Search for similar or related products"
      ]
    },
    "no-history": {
      icon: TrendingUp,
      title: "No search history yet",
      description: "Your recently analyzed products will appear here for quick access.",
      suggestions: []
    },
    "no-shortlist": {
      icon: ShoppingBag,
      title: "Your shortlist is empty",
      description: "Add products to your shortlist to compare them side by side.",
      suggestions: []
    }
  };

  const config = configs[type];
  const Icon = config.icon;

  return (
    <div style={{
      textAlign: 'center',
      padding: 'var(--space-2xl)',
      maxWidth: '600px',
      margin: '0 auto'
    }}>
      <div style={{
        width: '80px',
        height: '80px',
        margin: '0 auto var(--space-xl)',
        background: 'var(--color-primary-soft)',
        borderRadius: 'var(--radius-2xl)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        animation: 'pulse 2s ease-in-out infinite'
      }}>
        <Icon size={40} style={{ color: 'var(--color-primary)' }} />
      </div>
      
      <h3 style={{
        fontSize: '1.5rem',
        marginBottom: 'var(--space-md)',
        color: 'var(--color-text-main)'
      }}>
        {config.title}
      </h3>
      
      <p style={{
        fontSize: '1rem',
        color: 'var(--color-text-secondary)',
        marginBottom: 'var(--space-xl)',
        lineHeight: 1.7
      }}>
        {config.description}
      </p>

      {config.suggestions.length > 0 && (
        <div style={{
          background: 'var(--glass-bg)',
          backdropFilter: 'var(--backdrop-blur)',
          borderRadius: 'var(--radius-xl)',
          padding: 'var(--space-lg)',
          border: '1px solid var(--glass-border)',
          textAlign: 'left'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-sm)',
            marginBottom: 'var(--space-md)',
            color: 'var(--color-primary)'
          }}>
            <Sparkles size={18} />
            <strong style={{ fontSize: '0.9375rem' }}>Pro Tips:</strong>
          </div>
          <ul style={{
            listStyle: 'none',
            padding: 0,
            margin: 0,
            display: 'flex',
            flexDirection: 'column',
            gap: 'var(--space-sm)'
          }}>
            {config.suggestions.map((suggestion, i) => (
              <li key={i} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 'var(--space-sm)',
                fontSize: '0.9375rem',
                color: 'var(--color-text-secondary)'
              }}>
                <span style={{
                  display: 'inline-block',
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: 'var(--color-primary)',
                  marginTop: '8px',
                  flexShrink: 0
                }} />
                <span>{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default EmptyState;
