import React from "react";
import { getAccessToken, setAccessToken, clearAccessToken, onAccessTokenChanged } from "./token";

export interface AuthUser {
  id: number;
  email: string;
}

interface AuthContextValue {
  token: string | null;
  user: AuthUser | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = React.createContext<AuthContextValue | null>(null);

const API_BASE = import.meta.env.VITE_API_BASE_URL || window.location.origin;

async function handleAuthJson(res: Response) {
  const data = await res.json();
  if (!res.ok) {
    const msg =
      typeof data?.detail === "string"
        ? data.detail
        : typeof data?.error?.message === "string"
          ? data.error.message
          : `Auth request failed (${res.status})`;
    throw new Error(msg);
  }
  return data;
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setTokenState] = React.useState<string | null>(() => getAccessToken());
  const [user, setUser] = React.useState<AuthUser | null>(null);
  const [loading, setLoading] = React.useState<boolean>(true);

  async function fetchMe(t: string) {
    const res = await fetch(`${API_BASE}/api/auth/me`, {
      headers: { Authorization: `Bearer ${t}` },
    });
    const data = await handleAuthJson(res);
    setUser(data as AuthUser);
  }

  React.useEffect(() => {
    const t = getAccessToken();
    if (!t) {
      setLoading(false);
      return;
    }
    fetchMe(t)
      .catch(() => {
        clearAccessToken("unauthorized");
        setTokenState(null);
        setUser(null);
      })
      .finally(() => setLoading(false));

    // Keep AuthProvider in sync if some other part of the app clears/sets the token.
    const unsubscribe = onAccessTokenChanged((nextToken, _reason) => {
      if (!nextToken) {
        setTokenState(null);
        setUser(null);
        return;
      }

      // If token changed, refresh /me.
      setTokenState(nextToken);
      fetchMe(nextToken).catch(() => {
        clearAccessToken("unauthorized");
        setTokenState(null);
        setUser(null);
      });
    });

    return () => unsubscribe();
  }, []);

  async function login(email: string, password: string) {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await handleAuthJson(res);
    setAccessToken(data.access_token, "login");
    setTokenState(data.access_token);
    setUser(data.user as AuthUser);
  }

  async function register(email: string, password: string) {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await handleAuthJson(res);
    setAccessToken(data.access_token, "login");
    setTokenState(data.access_token);
    setUser(data.user as AuthUser);
  }

  function logout() {
    clearAccessToken("logout");
    setTokenState(null);
    setUser(null);
  }

  const value: AuthContextValue = {
    token,
    user,
    loading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export function useAuth(): AuthContextValue {
  const ctx = React.useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
