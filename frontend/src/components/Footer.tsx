
import React from "react";
import { Link } from "react-router-dom";
import {
  Zap,
  Mail,
  Phone,
  Clock,
  MapPin,
  Facebook,
  Twitter,
  Linkedin,
  Github,
  Heart
} from "lucide-react";

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="site-footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <div className="footer-brand">
              <div className="footer-logo">
                <Zap size={28} strokeWidth={3} />
              </div>
              <h3>ReviewAI Pro</h3>
            </div>
            <p className="footer-description">
              Your trusted AI-powered companion for making informed shopping decisions.
              We analyze thousands of reviews to bring you comprehensive product insights.
            </p>
            <div className="social-links">
              <a href="#" aria-label="Facebook" className="social-link">
                <Facebook size={20} />
              </a>
              <a href="#" aria-label="Twitter" className="social-link">
                <Twitter size={20} />
              </a>
              <a href="#" aria-label="LinkedIn" className="social-link">
                <Linkedin size={20} />
              </a>
              <a href="#" aria-label="GitHub" className="social-link">
                <Github size={20} />
              </a>
            </div>
          </div>

          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul className="footer-links">
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/about">About Us</Link>
              </li>
              <li>
                <Link to="/features">Features</Link>
              </li>
              <li>
                <Link to="/reviews">Start Review</Link>
              </li>
              <li>
                <Link to="/contact">Contact</Link>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Features</h4>
            <ul className="footer-links">
              <li>
                <Link to="/features#ai-analysis">AI-Powered Analysis</Link>
              </li>
              <li>
                <Link to="/features#sentiment">Sentiment Analysis</Link>
              </li>
              <li>
                <Link to="/features#comparison">Product Comparison</Link>
              </li>
              <li>
                <Link to="/features#pricing">Price Tracking</Link>
              </li>
              <li>
                <Link to="/features#alternatives">Smart Alternatives</Link>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Contact Info</h4>
            <div className="contact-info">
              <div className="contact-item">
                <Mail size={18} />
                <span>contact@reviewAI.com</span>
              </div>
              <div className="contact-item">
                <Phone size={18} />
                <span>08012345678</span>
              </div>
              <div className="contact-item">
                <Clock size={18} />
                <span>Mon-Fri, 9AM-5PM</span>
              </div>
              <div className="contact-item">
                <MapPin size={18} />
                <span>Lagos, Nigeria</span>
              </div>
            </div>
            <div className="newsletter">
              <h5>Subscribe to our Newsletter</h5>
              <form className="newsletter-form" onSubmit={(e) => e.preventDefault()}>
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="newsletter-input"
                />
                <button type="submit" className="newsletter-btn">
                  Subscribe
                </button>
              </form>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <p className="copyright">
              © {currentYear} ReviewAI Pro. All rights reserved.
            </p>
            <div className="footer-bottom-links">
              <Link to="/privacy">Privacy Policy</Link>
              <span className="separator">•</span>
              <Link to="/terms">Terms of Service</Link>
              <span className="separator">•</span>
              <Link to="/cookies">Cookie Policy</Link>
            </div>
            <p className="made-with">
              Made with <Heart size={16} className="heart-icon" /> by ReviewAI Team
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;