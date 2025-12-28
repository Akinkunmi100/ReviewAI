import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Zap, Search, Star, TrendingUp, ShieldCheck, BarChart2, Users, Award, ArrowRight, PlayCircle, MapPin, Clock } from "lucide-react";
import TypewriterText from "../components/TypewriterText";
import { apiStats, type StatsResponse } from "../api/client";

const HomePage: React.FC = () => {
  const [statsData, setStatsData] = useState<StatsResponse | null>(null);

  useEffect(() => {
    apiStats()
      .then(setStatsData)
      .catch((err) => console.error("Failed to fetch stats:", err));
  }, []);

  const features = [
    {
      icon: <Search size={32} />,
      title: "AI-Powered Analysis",
      description: "Our advanced AI analyzes thousands of reviews to provide comprehensive product insights.",
    },
    {
      icon: <Star size={32} />,
      title: "Smart Ratings",
      description: "Get accurate, unbiased ratings based on real user experiences and sentiment analysis.",
    },
    {
      icon: <TrendingUp size={32} />,
      title: "Price Tracking",
      description: "Monitor price trends and get alerts when products reach your target price.",
    },
    {
      icon: <ShieldCheck size={32} />,
      title: "Risk Assessment",
      description: "Identify potential risks and issues before making your purchase decision.",
    },
    {
      icon: <BarChart2 size={32} />,
      title: "Product Comparison",
      description: "Compare multiple products side-by-side to find the best option for your needs.",
    },
    {
      icon: <Users size={32} />,
      title: "Personalized Recommendations",
      description: "Get tailored suggestions based on your preferences and usage patterns.",
    },
  ];

  const benefits = [
    {
      title: "Unbiased Analysis",
      description: "We don't sell products. Our only goal is to give you the truth based on data, not sales commissions.",
      icon: <ShieldCheck size={32} />
    },
    {
      title: "Nigerian Market Focus",
      description: "Prices, availability, and context tailored specifically for Jumia, Konga, Slot, and local retailers.",
      icon: <MapPin size={32} />
    },
    {
      title: "Save Time & Money",
      description: "Stop wasting hours researching forums. Get the best validated deals in seconds.",
      icon: <Clock size={32} />
    }
  ];

  // Derive display values from real stats or show loading state
  const stats = [
    {
      value: statsData ? statsData.products_analyzed.toLocaleString() : "...",
      label: "Products Analyzed"
    },
    {
      // Multiplier logic from backend key, or just raw reviews if available. 
      // The backend "reviews_processed" is estimated at 10x products. 
      value: statsData ? statsData.reviews_processed.toLocaleString() : "...",
      label: "Insights Generated"
    },
    {
      value: "98%",
      label: "Analysis Accuracy"
    },
    {
      value: "24/7",
      label: "Real-time AI"
    }
  ];

  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <div className="hero-badge">
              <Zap size={24} />
              <span>AI-Powered Shopping Assistant</span>
            </div>
            <h1 className="hero-title">
              <TypewriterText
                text="Make Smarter Shopping Decisions with AI-Powered Insights"
                speed="normal"
                delay={300}
                cursor={true}
                highlightText="AI-Powered Insights"
              />
            </h1>
            <p className="hero-subtitle">
              ReviewAI Pro analyzes thousands of reviews to help you find the perfect products with confidence.
            </p>
            <div className="hero-actions">
              <Link to="/reviews" className="btn-primary">
                Start Your Review <ArrowRight size={18} />
              </Link>
              <Link to="/features" className="btn-secondary">
                Learn More <ArrowRight size={18} />
              </Link>
            </div>
            <div className="hero-stats">
              {stats.map((stat, index) => (
                <div key={index} className="stat-item">
                  <div className="stat-value">{stat.value}</div>
                  <div className="stat-label">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-mockup">
              <div className="mockup-content">
                <div className="mockup-header">
                  <div className="mockup-logo">
                    <Zap size={20} />
                  </div>
                  <span>Product Analysis Dashboard</span>
                  <div className="mockup-window-controls">
                    <div className="window-dot dot-red"></div>
                    <div className="window-dot dot-yellow"></div>
                    <div className="window-dot dot-green"></div>
                  </div>
                </div>

                <div className="dashboard-container">
                  {/* Sidebar Simulation */}
                  <div className="dashboard-sidebar">
                    {["Overview", "Sentiment", "Price", "Risks"].map((item, i) => (
                      <div key={i} className={`sidebar-item ${i === 0 ? 'active' : ''}`}>
                        {item}
                      </div>
                    ))}
                  </div>

                  {/* Main Chart Area */}
                  <div className="dashboard-main">
                    <div className="dashboard-header">
                      <div>
                        <div className="stat-trend-label">Sentiment Trend</div>
                        <div className="stat-trend-value">
                          +24% <span className="trend-up">↑</span>
                        </div>
                      </div>
                      <div className="rating-badge">Excellent</div>
                    </div>

                    <div className="chart-container-svg">
                      <svg width="100%" height="100%" viewBox="0 0 300 120" preserveAspectRatio="none">
                        <defs>
                          <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.3" />
                            <stop offset="100%" stopColor="var(--color-primary)" stopOpacity="0" />
                          </linearGradient>
                        </defs>
                        <path
                          d="M0,80 C30,75 50,40 80,45 C110,50 130,85 160,70 C190,55 220,20 250,30 C280,40 300,10 300,10 V120 H0 Z"
                          className="chart-path-fill"
                        />
                        <path
                          d="M0,80 C30,75 50,40 80,45 C110,50 130,85 160,70 C190,55 220,20 250,30 C280,40 300,10 300,10"
                          className="chart-path-stroke"
                        />
                        {/* Data Points */}
                        {[45, 70, 30].map((y, i) => (
                          <circle key={i} cx={80 + i * 85} cy={y} r="4" className="chart-point" />
                        ))}
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="features-container">
          <div className="section-header">
            <div className="section-badge">
              <Star size={20} />
              <span>Powerful Features</span>
            </div>
            <h2>Everything You Need for Smart Shopping</h2>
            <p className="section-subtitle">
              Our comprehensive suite of tools helps you make informed decisions with confidence.
            </p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="how-it-works">
        <div className="how-it-works-container">
          <div className="section-header">
            <div className="section-badge">
              <Zap size={20} />
              <span>How It Works</span>
            </div>
            <h2>Simple 3-Step Process</h2>
            <p className="section-subtitle">
              Get comprehensive product insights in just a few clicks.
            </p>
          </div>
          <div className="steps-container">
            <div className="step-card">
              <div className="step-number">1</div>
              <div className="step-icon">
                <Search size={36} />
              </div>
              <h3>Search for Products</h3>
              <p>Enter the product name or URL you want to analyze.</p>
            </div>
            <div className="step-arrow">
              <ArrowRight size={24} />
            </div>
            <div className="step-card">
              <div className="step-number">2</div>
              <div className="step-icon">
                <BarChart2 size={36} />
              </div>
              <h3>AI Analysis</h3>
              <p>Our AI analyzes thousands of reviews and data points.</p>
            </div>
            <div className="step-arrow">
              <ArrowRight size={24} />
            </div>
            <div className="step-card">
              <div className="step-number">3</div>
              <div className="step-icon">
                <ShieldCheck size={36} />
              </div>
              <h3>Make Confident Decision</h3>
              <p>Get comprehensive insights and make your purchase with confidence.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Replaced Testimonials with Benefits Section */}
      <section className="testimonials-section">
        <div className="testimonials-container">
          <div className="section-header">
            <div className="section-badge">
              <Award size={20} />
              <span>Why Choose Us</span>
            </div>
            <h2>Trusted by Smart Shoppers</h2>
            <p className="section-subtitle">
              We bring transparency and intelligence to the shopping experience.
            </p>
          </div>
          <div className="features-grid">
            {benefits.map((benefit, index) => (
              <div key={index} className="feature-card" style={{ textAlign: "center", alignItems: "center" }}>
                <div className="feature-icon" style={{ margin: "0 auto 16px" }}>{benefit.icon}</div>
                <h3 style={{ marginBottom: "12px" }}>{benefit.title}</h3>
                <p>{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-container">
          <div className="cta-content">
            <div className="cta-badge">
              <Zap size={20} />
              <span>Ready to Shop Smarter?</span>
            </div>
            <h2>Start Making Better Purchasing Decisions Today</h2>
            <p>Join smart shoppers who trust ReviewAI Pro for comprehensive product insights.</p>
            <div className="cta-actions">
              <Link to="/reviews" className="btn-primary">
                Start Your Free Analysis <ArrowRight size={18} />
              </Link>
              <Link to="/features" className="btn-secondary">
                Explore All Features <ArrowRight size={18} />
              </Link>
            </div>
          </div>
          <div className="cta-visual">
            <div className="cta-mockup">
              <div className="mockup-phone">
                <div className="phone-screen">
                  <div className="phone-header">
                    <div className="phone-logo">
                      <Zap size={16} />
                    </div>
                    <span>ReviewAI Pro</span>
                  </div>
                  <div className="phone-content">
                    <div className="gauge-container">
                      <div className="gauge-svg-wrapper">
                        <svg width="160" height="80" viewBox="0 0 200 100">
                          {/* Background Arc */}
                          <path d="M10,100 A90,90 0 0,1 190,100" fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth="20" />
                          {/* Value Arc (75% filled) */}
                          <path d="M10,100 A90,90 0 0,1 165,35" fill="none" stroke="var(--color-primary)" strokeWidth="20" strokeLinecap="round" />
                        </svg>
                        <div className="gauge-score">
                          <span className="trust-score-text">94%</span>
                        </div>
                      </div>

                      <div className="gauge-label">
                        <h4>Excellent Choice</h4>
                        <p>Trust Score</p>
                      </div>

                      <div className="loading-bars">
                        {[1, 2].map((_, i) => (
                          <div key={i} className="loading-bar" style={{
                            width: i === 0 ? "80%" : "60%"
                          }}></div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;