import React from "react";
import { Link } from "react-router-dom";
import { Zap, Users, Award, Target, Lightbulb, Heart, ArrowRight, ShieldCheck } from "lucide-react";
import TypewriterText from "../components/TypewriterText";

const AboutPage: React.FC = () => {
  const values = [
    {
      icon: <Target size={28} />,
      title: "Accuracy",
      description: "We provide unbiased, data-driven insights you can trust.",
    },
    {
      icon: <Users size={28} />,
      title: "User-Centric",
      description: "Our users are at the heart of everything we do.",
    },
    {
      icon: <Lightbulb size={28} />,
      title: "Innovation",
      description: "We constantly push the boundaries of AI-powered analysis.",
    },
    {
      icon: <Heart size={28} />,
      title: "Integrity",
      description: "We maintain transparency and ethical practices in all our work.",
    },
  ];

  return (
    <div className="about-page">
      <section className="about-hero">
        <div className="about-hero-container">
          <div className="about-hero-content">
            <div className="about-badge">
              <Zap size={20} />
              <span>Our Story</span>
            </div>
            <h1>
              <TypewriterText
                text="Empowering Smart Shoppers with AI-Powered Insights"
                speed="normal"
                delay={200}
                cursor={true}
                highlightText="AI-Powered Insights"
              />
            </h1>
            <p className="about-subtitle">
              At ReviewAI Pro, we believe that every purchase should be made with confidence.
              Our mission is to provide comprehensive, unbiased product insights using cutting-edge AI technology, tailored specifically for the Nigerian market.
            </p>
            <div className="about-actions">
              <Link to="/features" className="btn-primary">
                Explore Features <ArrowRight size={18} />
              </Link>
              <Link to="/contact" className="btn-secondary">
                Get in Touch <ArrowRight size={18} />
              </Link>
            </div>
          </div>
          <div className="about-hero-visual">
            <div className="about-mockup">
              <div className="mockup-team" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', padding: '2rem' }}>
                <ShieldCheck size={64} color="#6366f1" style={{ marginBottom: '1rem' }} />
                <h3 style={{ margin: 0 }}>Trusted & Secure</h3>
                <p style={{ margin: '0.5rem 0 0', opacity: 0.7 }}>Data-Driven Analysis</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="about-mission">
        <div className="about-mission-container">
          <div className="mission-content">
            <div className="mission-icon">
              <Zap size={48} />
            </div>
            <h2>Our Mission</h2>
            <p>
              We founded ReviewAI Pro to solve a common problem: the overwhelming amount of information
              available when making purchasing decisions. Our AI-powered platform analyzes thousands of
              reviews, specifications, and user experiences to provide you with clear, actionable insights.
            </p>
            <p>
              Whether you're buying electronics, appliances, or any other product, ReviewAI Pro helps you
              make informed decisions with confidence, saving you time and money.
            </p>
          </div>
        </div>
      </section>

      <section className="about-values">
        <div className="about-values-container">
          <div className="section-header">
            <div className="section-badge">
              <Award size={20} />
              <span>Core Values</span>
            </div>
            <h2>What Drives Us</h2>
            <p className="section-subtitle">
              Our values guide everything we do and help us deliver the best possible experience to our users.
            </p>
          </div>
          <div className="values-grid">
            {values.map((value, index) => (
              <div key={index} className="value-card">
                <div className="value-icon">{value.icon}</div>
                <h3>{value.title}</h3>
                <p>{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="about-cta">
        <div className="about-cta-container">
          <div className="cta-content">
            <div className="cta-badge">
              <Zap size={20} />
              <span>Join Our Mission</span>
            </div>
            <h2>Be Part of the Smart Shopping Revolution</h2>
            <p>
              Whether you're a user looking for better purchasing decisions or interested in our technology,
              we'd love to hear from you.
            </p>
            <div className="cta-actions">
              <Link to="/contact" className="btn-primary">
                Contact Us <ArrowRight size={18} />
              </Link>
              <Link to="/reviews" className="btn-secondary">
                Try ReviewAI Pro <ArrowRight size={18} />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;