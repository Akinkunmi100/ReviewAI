import type { EnhancedProductReview, ProductComparison } from "./types";
import type { UserProfile } from "../components/ProfilePanel";
import { getAccessToken, clearAccessToken } from "../auth/token";

const API_BASE = import.meta.env.VITE_API_BASE_URL || window.location.origin;

function authHeaders(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handleJson<T>(res: Response): Promise<T> {
  const data = await res.json();
  const rawError = (data as any).error;

  const normalizeError = (value: any): string | null => {
    if (!value) return null;
    if (typeof value === "string") return value;
    if (typeof value === "object" && typeof value.message === "string") return value.message;
    return JSON.stringify(value);
  };

  const message = normalizeError(rawError);

  if (!res.ok) {
    if (res.status === 401) {
      // Token expired/invalid; clear it so RequireAuth can redirect.
      clearAccessToken("unauthorized");
    }
    throw new Error(message || `Request failed with status ${res.status}`);
  }
  if (message) {
    throw new Error(message);
  }
  return data as T;
}

export async function apiReview(
  productName: string,
  dataMode: "web" | "ai" | "hybrid" = "web",
  userId?: string,
): Promise<EnhancedProductReview> {
  const res = await fetch(`${API_BASE}/api/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({
      product_name: productName,
      data_mode: dataMode,
      user_id: userId ?? null,
    }),
  });
  return handleJson<EnhancedProductReview>(res);
}

export async function apiCompare(
  products: string[],
): Promise<ProductComparison> {
  const res = await fetch(`${API_BASE}/api/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ products }),
  });
  return handleJson<ProductComparison>(res);
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ApiChatParams {
  productName: string;
  message: string;
  history: ChatMessage[];
  dataMode?: "web" | "ai" | "hybrid";
  userProfile?: UserProfile | null;
  userId?: string;
  sessionId?: number | null;
}

export interface ApiChatResponse {
  reply: string;
  session_id?: number;
}

export async function apiChat(params: ApiChatParams): Promise<ApiChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({
      product_name: params.productName,
      message: params.message,
      conversation_history: params.history,
      data_mode: params.dataMode ?? "web",
      user_profile: params.userProfile ?? null,
      user_id: params.userId ?? null,
      session_id: params.sessionId ?? null,
    }),
  });
  return handleJson<ApiChatResponse>(res);
}

export interface StatsResponse {
  products_analyzed: number;
  reviews_processed: number;
  active_users: number;
}

export async function apiStats(): Promise<StatsResponse> {
  const res = await fetch(`${API_BASE}/api/stats`, { headers: { ...authHeaders() } });
  return handleJson<StatsResponse>(res);
}

// =============================================================================
// Profile API (requires authentication)
// =============================================================================

export async function apiSaveProfile(
  profile: UserProfile,
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({
      min_budget: profile.min_budget ?? null,
      max_budget: profile.max_budget ?? null,
      use_cases: profile.use_cases ?? [],
      preferred_brands: profile.preferred_brands ?? [],
    }),
  });
  await handleJson<{ status: string }>(res);
}

export async function apiGetProfile(): Promise<UserProfile | null> {
  try {
    const res = await fetch(`${API_BASE}/api/profile`, {
      headers: { ...authHeaders() },
    });
    if (!res.ok) {
      return null;
    }
    const data = await res.json();
    if (!data || Object.keys(data).length === 0) {
      return null;
    }
    return {
      min_budget: data.min_budget ?? null,
      max_budget: data.max_budget ?? null,
      use_cases: data.use_cases ?? [],
      preferred_brands: data.preferred_brands ?? [],
    };
  } catch {
    return null;
  }
}

