const TOKEN_KEY = "product-review-access-token";
const TOKEN_EVENT = "auth-token-changed";

export type TokenChangeReason = "login" | "logout" | "unauthorized" | "unknown";

function emitTokenChanged(token: string | null, reason: TokenChangeReason) {
  try {
    window.dispatchEvent(new CustomEvent(TOKEN_EVENT, { detail: { token, reason } }));
  } catch {
    // ignore
  }
}

export function getAccessToken(): string | null {
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setAccessToken(token: string, reason: TokenChangeReason = "login") {
  window.localStorage.setItem(TOKEN_KEY, token);
  emitTokenChanged(token, reason);
}

export function clearAccessToken(reason: TokenChangeReason = "logout") {
  window.localStorage.removeItem(TOKEN_KEY);
  emitTokenChanged(null, reason);
}

export function onAccessTokenChanged(
  handler: (token: string | null, reason: TokenChangeReason) => void,
): () => void {
  const listener = (evt: Event) => {
    const ce = evt as CustomEvent;
    handler(
      (ce.detail?.token as string | null) ?? null,
      (ce.detail?.reason as TokenChangeReason) ?? "unknown",
    );
  };

  window.addEventListener(TOKEN_EVENT, listener);
  return () => window.removeEventListener(TOKEN_EVENT, listener);
}
