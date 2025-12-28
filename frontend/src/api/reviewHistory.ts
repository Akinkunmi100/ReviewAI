import { getAccessToken, clearAccessToken } from "../auth/token";
import type { EnhancedProductReview } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || window.location.origin;

function authHeaders(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function fetchSavedReview(
  productName: string,
): Promise<EnhancedProductReview | null> {
  const res = await fetch(`${API_BASE}/api/history/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ product_name: productName }),
  });

  if (!res.ok) {
    if (res.status === 401) clearAccessToken("unauthorized");
    throw new Error(`Failed to load saved review: ${res.status}`);
  }

  const data = await res.json();
  return (data.review as EnhancedProductReview | null) ?? null;
}
