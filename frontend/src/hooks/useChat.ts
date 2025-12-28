import { useEffect, useState, useRef } from "react";
import { apiChat, ChatMessage } from "../api/client";
import type { UserProfile } from "../components/ProfilePanel";

interface UseChatOptions {
  sessionId?: number | null;
  initialHistory?: ChatMessage[];
  userId?: string;
}

export function useChat(
  productName: string,
  dataMode: "web" | "ai" | "hybrid" = "web",
  userProfile?: UserProfile | null,
  options: UseChatOptions = {},
) {
  const [messages, setMessages] = useState<ChatMessage[]>(
    options.initialHistory ?? [],
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<number | null>(
    options.sessionId ?? null,
  );

  // Use ref to always have the latest userProfile value
  const userProfileRef = useRef(userProfile);
  
  // Update ref whenever userProfile changes
  useEffect(() => {
    userProfileRef.current = userProfile;
  }, [userProfile]);

  useEffect(() => {
    if (options.initialHistory) {
      setMessages(options.initialHistory);
    }
    if (options.sessionId !== undefined) {
      setSessionId(options.sessionId ?? null);
    }
  }, [options.initialHistory, options.sessionId]);

  async function sendMessage(text: string) {
    const newMessages: ChatMessage[] = [...messages, { role: "user" as const, content: text }];
    setMessages(newMessages);
    setLoading(true);
    setError(null);

    try {
        // Use the ref to get the latest profile value
        const { reply, session_id } = await apiChat({
          productName,
          message: text,
          history: newMessages,
          dataMode,
          userProfile: userProfileRef.current, // ✅ Always use the latest profile
          userId: options.userId,
          sessionId,
        });

      if (session_id && session_id !== sessionId) {
        setSessionId(session_id);
      }

      setMessages([...newMessages, { role: "assistant" as const, content: reply }]);
    } catch (e: any) {
      setError(e.message ?? "Chat error");
    } finally {
      setLoading(false);
    }
  }

  return { messages, loading, error, sendMessage, sessionId };
}
