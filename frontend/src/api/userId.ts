export function getUserId(): string {
  // Use a stable key in localStorage so the user retains their profile/shortlist/chat when not logged in
  const key = "taofeek_user_id";
  let id = localStorage.getItem(key);
  if (!id) {
    // Use the browser crypto API for secure randomness
    if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
      id = crypto.randomUUID();
    } else {
      id = `${Date.now().toString(36)}-${Math.random().toString(36).substring(2, 10)}`;
    }
    localStorage.setItem(key, id);
  }
  return id;
}
