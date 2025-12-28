import React from "react";
import { Link } from "react-router-dom";
import { Zap, Mail, Phone, MapPin, Send, User, MessageCircle, Clock, ArrowRight, Check } from "lucide-react";

const ContactPage: React.FC = () => {
  const [formData, setFormData] = React.useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [submitStatus, setSubmitStatus] = React.useState<"success" | "error" | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus(null);

    // Simulate form submission
    try {
      await new Promise((resolve) => setTimeout(resolve, 1500));
      setSubmitStatus("success");
      setFormData({ name: "", email: "", subject: "", message: "" });
    } catch (error) {
      setSubmitStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactMethods = [
    {
      icon: <Mail size={24} />,
      title: "Email Support",
      description: "Get quick responses to your questions and concerns.",
      contact: "contact@taofeek.com",
    },
    {
      icon: <Phone size={24} />,
      title: "Phone Support",
      description: "Speak directly with our support team during business hours.",
      contact: "08012345678",
    },
    {
      icon: <MessageCircle size={24} />,
      title: "Live Chat",
      description: "Get instant help through our live chat feature.",
      contact: "Available Mon-Fri, 9AM-5PM",
    },
  ];

  const faqItems = [
    {
      question: "How does ReviewAI Pro work?",
      answer: "ReviewAI Pro uses advanced AI algorithms to analyze thousands of reviews from multiple sources, providing comprehensive insights and ratings for products.",
    },
    {
      question: "Is ReviewAI Pro free to use?",
      answer: "Yes, ReviewAI Pro offers a free tier with basic features. We also have premium plans for advanced functionality and business users.",
    },
    {
      question: "How accurate are the reviews?",
      answer: "Our AI analyzes thousands of data points to provide highly accurate insights. We continuously improve our algorithms to ensure the best possible results.",
    },
    {
      question: "Can I use ReviewAI Pro for business purposes?",
      answer: "Absolutely! We offer special business plans with advanced features tailored for professional use.",
    },
  ];

  return (
    <div className="contact-page">
      <section className="contact-hero">
        <div className="contact-hero-container">
          <div className="contact-hero-content">
            <div className="contact-badge">
              <Zap size={20} />
              <span>Get in Touch</span>
            </div>
            <h1>We'd Love to Hear From You</h1>
            <p className="contact-subtitle">
              Have questions, feedback, or just want to say hello? Our team is ready to assist you.
            </p>
            <div className="contact-actions">
              <Link to="/reviews" className="btn-primary">
                Try ReviewAI Pro <ArrowRight size={18} />
              </Link>
              <Link to="/features" className="btn-secondary">
                Explore Features <ArrowRight size={18} />
              </Link>
            </div>
          </div>
          <div className="contact-hero-visual">
            <div className="contact-mockup">
              <div className="mockup-contact">
                <div className="contact-info-card">
                  <div className="contact-icon">
                    <Mail size={32} />
                  </div>
                  <span className="contact-label">Email</span>
                  <span className="contact-value">contact@taofeek.com</span>
                </div>
                <div className="contact-info-card">
                  <div className="contact-icon">
                    <Phone size={32} />
                  </div>
                  <span className="contact-label">Phone</span>
                  <span className="contact-value">08012345678</span>
                </div>
                <div className="contact-info-card">
                  <div className="contact-icon">
                    <Clock size={32} />
                  </div>
                  <span className="contact-label">Hours</span>
                  <span className="contact-value">Mon-Fri, 9AM-5PM</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="contact-methods">
        <div className="contact-methods-container">
          <div className="section-header">
            <div className="section-badge">
              <Mail size={20} />
              <span>Contact Options</span>
            </div>
            <h2>Multiple Ways to Reach Us</h2>
            <p className="section-subtitle">
              Choose the contact method that works best for you.
            </p>
          </div>
          <div className="methods-grid">
            {contactMethods.map((method, index) => (
              <div key={index} className="method-card">
                <div className="method-icon">{method.icon}</div>
                <h3>{method.title}</h3>
                <p>{method.description}</p>
                <div className="method-contact">
                  <span>{method.contact}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="contact-form-section">
        <div className="contact-form-container">
          <div className="form-header">
            <div className="form-badge">
              <Send size={20} />
              <span>Send Us a Message</span>
            </div>
            <h2>Contact Form</h2>
            <p>Fill out the form below and we'll get back to you as soon as possible.</p>
          </div>
          <div className="form-content">
            <form onSubmit={handleSubmit} className="contact-form">
              <div className="form-group">
                <label htmlFor="name">Your Name</label>
                <div className="input-wrapper">
                  <User size={18} className="input-icon" />
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Enter your name"
                    required
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <div className="input-wrapper">
                  <Mail size={18} className="input-icon" />
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    required
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="subject">Subject</label>
                <div className="input-wrapper">
                  <MessageCircle size={18} className="input-icon" />
                  <input
                    type="text"
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    placeholder="Enter subject"
                    required
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="message">Your Message</label>
                <div className="input-wrapper">
                  <MessageCircle size={18} className="input-icon" />
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Enter your message"
                    rows={5}
                    required
                  />
                </div>
              </div>
              <button
                type="submit"
                className="btn-primary submit-btn"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <span className="loading-spinner"></span>
                    Sending...
                  </>
                ) : (
                  <>
                    Send Message <Send size={18} />
                  </>
                )}
              </button>
              {submitStatus === "success" && (
                <div className="form-success">
                  <Check size={18} />
                  <span>Message sent successfully! We'll get back to you soon.</span>
                </div>
              )}
              {submitStatus === "error" && (
                <div className="form-error">
                  <span>There was an error sending your message. Please try again.</span>
                </div>
              )}
            </form>
            <div className="form-visual">
              <div className="form-mockup">
                <div className="mockup-message">
                  <div className="message-icon">
                    <Send size={48} />
                  </div>
                  <span className="message-text">Your message is on its way!</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="contact-faq">
        <div className="contact-faq-container">
          <div className="section-header">
            <div className="section-badge">
              <Zap size={20} />
              <span>Frequently Asked Questions</span>
            </div>
            <h2>Common Questions</h2>
            <p className="section-subtitle">
              Find answers to frequently asked questions about ReviewAI Pro.
            </p>
          </div>
          <div className="faq-grid">
            {faqItems.map((item, index) => (
              <div key={index} className="faq-item">
                <div className="faq-question">
                  <h3>{item.question}</h3>
                </div>
                <div className="faq-answer">
                  <p>{item.answer}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="contact-cta">
        <div className="contact-cta-container">
          <div className="cta-content">
            <div className="cta-badge">
              <Zap size={20} />
              <span>Need Immediate Help?</span>
            </div>
            <h2>Start Using ReviewAI Pro Today</h2>
            <p>
              Experience the power of AI-driven shopping assistance and make better purchasing decisions.
            </p>
            <div className="cta-actions">
              <Link to="/reviews" className="btn-primary">
                Start Your Free Analysis <ArrowRight size={18} />
              </Link>
              <Link to="/features" className="btn-secondary">
                Learn More About Features <ArrowRight size={18} />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ContactPage;