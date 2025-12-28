import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Zap, Home, Info, Star, Mail, Search, Menu, X, LogIn, User, LogOut } from "lucide-react";
import { useAuth } from "../auth/AuthContext";

interface HeaderProps {
  theme: "light" | "dark";
  toggleTheme: () => void;
}

const Header: React.FC<HeaderProps> = ({ theme, toggleTheme }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { token, user, logout } = useAuth();

  const navLinks = [
    { path: "/", label: "Home", icon: Home },
    { path: "/about", label: "About", icon: Info },
    { path: "/features", label: "Features", icon: Star },
    { path: "/reviews", label: "Reviews", icon: Search },
    { path: "/contact", label: "Contact", icon: Mail },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="site-header">
      <div className="header-container">
        <Link to="/" className="logo-wrapper">
          <div className="logo-badge">
            <Zap size={24} strokeWidth={3} />
          </div>
          <div className="logo-text">
            <span className="logo-title">ReviewAI Pro</span>
            <span className="logo-tagline">Smart Shopping Decisions</span>
          </div>
        </Link>

        <nav className={`nav-menu ${mobileMenuOpen ? "mobile-open" : ""}`}>
          {navLinks.map((link) => {
            const Icon = link.icon;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`nav-link ${isActive(link.path) ? "active" : ""}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <Icon size={18} />
                <span>{link.label}</span>
              </Link>
            );
          })}

          {/* Mobile auth actions (desktop uses header-actions) */}
          <div className="mobile-auth-actions">
            {token ? (
              <button
                type="button"
                className="nav-link"
                onClick={() => {
                  logout();
                  setMobileMenuOpen(false);
                  navigate("/", { replace: true });
                }}
              >
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            ) : (
              <>
                <Link
                  to="/login"
                  className={`nav-link ${isActive("/login") ? "active" : ""}`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <LogIn size={18} />
                  <span>Login</span>
                </Link>
                <Link
                  to="/register"
                  className={`nav-link ${isActive("/register") ? "active" : ""}`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <User size={18} />
                  <span>Register</span>
                </Link>
              </>
            )}
          </div>
        </nav>

        <div className="header-actions">
          <div className="auth-actions">
            {token ? (
              <>
                <button
                  type="button"
                  className="auth-user"
                  onClick={() => navigate("/reviews")}
                  title={user?.email ?? "Account"}
                >
                  <User size={16} />
                  <span>{user?.email ?? "Account"}</span>
                </button>
                <button
                  type="button"
                  className="auth-logout"
                  onClick={() => {
                    logout();
                    navigate("/", { replace: true });
                  }}
                  title="Logout"
                >
                  <LogOut size={16} />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="auth-link">
                  <LogIn size={16} />
                  <span>Login</span>
                </Link>
                <Link to="/register" className="auth-link auth-link-primary">
                  <span>Register</span>
                </Link>
              </>
            )}
          </div>

          <button
            className="theme-toggle-btn"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === "dark" ? (
              <>
                <svg className="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="5"/>
                  <line x1="12" y1="1" x2="12" y2="3"/>
                  <line x1="12" y1="21" x2="12" y2="23"/>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                  <line x1="1" y1="12" x2="3" y2="12"/>
                  <line x1="21" y1="12" x2="23" y2="12"/>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
              </>
            ) : (
              <>
                <svg className="moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
              </>
            )}
          </button>

          <button
            className="mobile-menu-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;