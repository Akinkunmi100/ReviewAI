import { getAccessToken, clearAccessToken } from "../auth/token";

const API_BASE = import.meta.env.VITE_API_BASE_URL || window.location.origin;

function authHeaders(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export interface ChatHistoryMessage {
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export async function fetchChatSession(
  userId: string | undefined,
  sessionId: number,
): Promise<ChatHistoryMessage[]> {
  const res = await fetch(`${API_BASE}/api/history/chat-session`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ user_id: userId ?? null, session_id: sessionId }),
  });

  if (!res.ok) {
    if (res.status === 401) clearAccessToken("unauthorized");
    throw new Error(`Failed to load chat session: ${res.status}`);
  }

  const data = await res.json();
  return data.messages ?? [];
}
