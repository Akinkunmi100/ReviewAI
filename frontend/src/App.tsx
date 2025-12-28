import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import GlobalAlert from "./components/GlobalAlert";
import { onAccessTokenChanged } from "./auth/token";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import FeaturesPage from "./pages/FeaturesPage";
import ContactPage from "./pages/ContactPage";
import ReviewPage from "./pages/ReviewPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import { AuthProvider } from "./auth/AuthContext";
import { RequireAuth } from "./auth/RequireAuth";

const App: React.FC = () => {
  const [theme, setTheme] = React.useState<"light" | "dark">(() => {
    if (typeof window !== "undefined") {
      const stored = window.localStorage.getItem("theme");
      if (stored === "light" || stored === "dark") return stored;
      if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        return "dark";
      }
    }
    return "light";
  });

  React.useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    try {
      window.localStorage.setItem("theme", theme);
    } catch {
      // ignore storage errors
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  const [sessionMessage, setSessionMessage] = React.useState<string | null>(null);

  React.useEffect(() => {
    // Show a friendly message when a token is cleared due to 401.
    const unsubscribe = onAccessTokenChanged((token, reason) => {
      if (!token && reason === "unauthorized") {
        setSessionMessage("Your session expired. Please log in again.");
      }
    });
    return () => unsubscribe();
  }, []);

  return (
    <AuthProvider>
      <Router>
        <div className="app-shell">
          <Header theme={theme} toggleTheme={toggleTheme} />
          <GlobalAlert message={sessionMessage} onClose={() => setSessionMessage(null)} />
          <main className="app-main">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/features" element={<FeaturesPage />} />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route
                path="/reviews"
                element={
                  <RequireAuth>
                    <ReviewPage />
                  </RequireAuth>
                }
              />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
