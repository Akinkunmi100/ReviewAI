import { getAccessToken, clearAccessToken } from "../auth/token";

const API_BASE = import.meta.env.VITE_API_BASE_URL || window.location.origin;

function authHeaders(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export interface ShortlistItem {
  product_name: string;
  created_at: string;
}

export async function fetchShortlist(): Promise<ShortlistItem[]> {
  const res = await fetch(`${API_BASE}/api/shortlist`, {
    headers: { ...authHeaders() },
  });
  if (!res.ok) {
    if (res.status === 401) clearAccessToken("unauthorized");
    throw new Error(`Failed to load shortlist: ${res.status}`);
  }
  return res.json();
}

export async function addToShortlist(productName: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/shortlist/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ product_name: productName }),
  });
  if (!res.ok) {
    if (res.status === 401) clearAccessToken("unauthorized");
    throw new Error(`Failed to add to shortlist: ${res.status}`);
  }
}

export async function removeFromShortlist(productName: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/shortlist/remove`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ product_name: productName }),
  });
  if (!res.ok) {
    if (res.status === 401) clearAccessToken("unauthorized");
    throw new Error(`Failed to remove from shortlist: ${res.status}`);
  }
}
