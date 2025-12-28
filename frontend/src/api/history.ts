import { getAccessToken, clearAccessToken } from "../auth/token";

const API_BASE = import.meta.env.VITE_API_BASE_URL || window.location.origin;

function authHeaders(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export interface ApiHistorySummary {
  products: {
    id: number;
    product_name: string;
    last_viewed_at: string;
    rating?: string | null;
    price?: number | string | null;
  }[];
  sessions: {
    id: number;
    product_name: string;
    created_at: string;
  }[];
}

export async function fetchHistorySummary(userId?: string): Promise<ApiHistorySummary> {
  const res = await fetch(`${API_BASE}/api/history/summary`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ user_id: userId ?? null }),
  });

  if (!res.ok) {
    if (res.status === 401) clearAccessToken("unauthorized");
    throw new Error(`Failed to load history: ${res.status}`);
  }

  return res.json();
}

export async function fetchLatestSession(
  userId: string | undefined,
  productName: string,
): Promise<number | null> {
  const res = await fetch(`${API_BASE}/api/history/latest-session`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ user_id: userId ?? null, product_name: productName }),
  });

  if (!res.ok) {
    if (res.status === 401) clearAccessToken("unauthorized");
    throw new Error(`Failed to load latest session: ${res.status}`);
  }

  const data = await res.json();
  return (data.session_id as number | null) ?? null;
}
