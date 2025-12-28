import React from "react";
import { Link } from "react-router-dom";
import { Zap, Search, Star, TrendingUp, ShieldCheck, BarChart2, Users, Award, ArrowRight, Check, Target, Database, Lightbulb, Clock, Heart } from "lucide-react";
import TypewriterText from "../components/TypewriterText";

const FeaturesPage: React.FC = () => {
  const features = [
    {
      id: "ai-analysis",
      icon: <Search size={32} />,
      title: "AI-Powered Analysis",
      description: "Our advanced AI analyzes thousands of reviews from multiple sources to provide comprehensive product insights.",
      details: [
        "Natural Language Processing for sentiment analysis",
        "Multi-source review aggregation",
        "Automated quality assessment",
        "Real-time data processing",
      ],
    },
    {
      id: "sentiment",
      icon: <Star size={32} />,
      title: "Sentiment Analysis",
      description: "Get detailed sentiment breakdowns across different product aspects.",
      details: [
        "Aspect-based sentiment analysis",
        "Positive/negative sentiment detection",
        "Emotion analysis",
        "Trend analysis over time",
      ],
    },
    {
      id: "comparison",
      icon: <BarChart2 size={32} />,
      title: "Product Comparison",
      description: "Compare multiple products side-by-side with detailed metrics.",
      details: [
        "Multi-product comparison",
        "Feature-by-feature analysis",
        "Price-performance ratio",
        "Visual comparison charts",
      ],
    },
    {
      id: "pricing",
      icon: <TrendingUp size={32} />,
      title: "Price Tracking",
      description: "Monitor price trends and get alerts for the best deals.",
      details: [
        "Historical price tracking",
        "Price drop alerts",
        "Price prediction algorithms",
        "Best time to buy recommendations",
      ],
    },
    {
      id: "alternatives",
      icon: <ShieldCheck size={32} />,
      title: "Smart Alternatives",
      description: "Find better alternatives based on your needs and budget.",
      details: [
        "Similar product recommendations",
        "Budget-friendly alternatives",
        "Feature-based matching",
        "User preference learning",
      ],
    },
    {
      id: "risk-assessment",
      icon: <Users size={32} />,
      title: "Risk Assessment",
      description: "Identify potential issues and risks before purchasing.",
      details: [
        "Common problem detection",
        "Reliability scoring",
        "Warranty analysis",
        "Return policy assessment",
      ],
    },
  ];

  const benefits = [
    {
      icon: <Target size={24} />,
      title: "Save Time",
      description: "Get comprehensive insights in seconds instead of hours of research.",
    },
    {
      icon: <Database size={24} />,
      title: "Data-Driven Decisions",
      description: "Make purchases based on real data, not just marketing claims.",
    },
    {
      icon: <Lightbulb size={24} />,
      title: "Discover Better Options",
      description: "Find products you might have overlooked that better suit your needs.",
    },
    {
      icon: <Clock size={24} />,
      title: "Avoid Buyer's Remorse",
      description: "Make purchases with confidence, knowing you've made the right choice.",
    },
    {
      icon: <Heart size={24} />,
      title: "Personalized Experience",
      description: "Get recommendations tailored to your specific preferences and needs.",
    },
    {
      icon: <ShieldCheck size={24} />,
      title: "Risk Mitigation",
      description: "Identify potential issues before making your purchase.",
    },
  ];

  return (
    <div className="features-page">
      <section className="features-hero">
        <div className="features-hero-container">
          <div className="features-hero-content">
            <div className="features-badge">
              <Zap size={20} />
              <span>Powerful Features</span>
            </div>
            <h1>
              <TypewriterText
                text="Comprehensive AI-Powered Shopping Assistant"
                speed="normal"
                delay={200}
                cursor={true}
                highlightText="AI-Powered"
              />
            </h1>
            <p className="features-subtitle">
              ReviewAI Pro offers a complete suite of tools to help you make informed purchasing decisions with confidence.
            </p>
            <div className="features-actions">
              <Link to="/reviews" className="btn-primary">
                Try It Now <ArrowRight size={18} />
              </Link>
              <Link to="/about" className="btn-secondary">
                Learn About Us <ArrowRight size={18} />
              </Link>
            </div>
          </div>
          <div className="features-hero-visual">
            <div className="features-mockup">
              <div className="mockup-dashboard">
                <div className="dashboard-cards">
                  <div className="dashboard-card">
                    <div className="card-icon">
                      <Search size={20} />
                    </div>
                    <span className="card-value">10,000+</span>
                    <span className="card-label">Reviews Analyzed</span>
                  </div>
                  <div className="dashboard-card">
                    <div className="card-icon">
                      <Star size={20} />
                    </div>
                    <span className="card-value">4.8</span>
                    <span className="card-label">Average Rating</span>
                  </div>
                  <div className="dashboard-card">
                    <div className="card-icon">
                      <ShieldCheck size={20} />
                    </div>
                    <span className="card-value">95%</span>
                    <span className="card-label">Confidence Score</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="features-grid-section">
        <div className="features-grid-container">
          <div className="section-header">
            <div className="section-badge">
              <Award size={20} />
              <span>Core Features</span>
            </div>
            <h2>Everything You Need for Smart Shopping</h2>
            <p className="section-subtitle">
              Our comprehensive feature set covers all aspects of product research and decision making.
            </p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card" id={feature.id}>
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
                <ul className="feature-details">
                  {feature.details.map((detail, detailIndex) => (
                    <li key={detailIndex}>
                      <Check size={16} />
                      <span>{detail}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="features-benefits">
        <div className="features-benefits-container">
          <div className="section-header">
            <div className="section-badge">
              <Heart size={20} />
              <span>Why Choose Us</span>
            </div>
            <h2>Benefits of Using ReviewAI Pro</h2>
            <p className="section-subtitle">
              Discover how ReviewAI Pro transforms your shopping experience.
            </p>
          </div>
          <div className="benefits-grid">
            {benefits.map((benefit, index) => (
              <div key={index} className="benefit-card">
                <div className="benefit-icon">{benefit.icon}</div>
                <h3>{benefit.title}</h3>
                <p>{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="features-cta">
        <div className="features-cta-container">
          <div className="cta-content">
            <div className="cta-badge">
              <Zap size={20} />
              <span>Ready to Experience?</span>
            </div>
            <h2>Start Making Better Purchasing Decisions Today</h2>
            <p>
              Join thousands of smart shoppers who trust ReviewAI Pro for comprehensive product insights.
              Experience the power of AI-driven shopping assistance.
            </p>
            <div className="cta-actions">
              <Link to="/reviews" className="btn-primary">
                Start Your Free Analysis <ArrowRight size={18} />
              </Link>
              <Link to="/contact" className="btn-secondary">
                Get a Personal Demo <ArrowRight size={18} />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default FeaturesPage;