import React, { useState, useRef, useEffect } from "react";
import type { ChatMessage } from "../api/client";
import { Send, User, Sparkles, Bot } from "lucide-react";
import MarkdownRenderer from "./MarkdownRenderer";

interface ChatHook {
  messages: ChatMessage[];
  loading: boolean;
  error: string | null;
  sendMessage: (text: string) => Promise<void>;
}

const ChatPanel: React.FC<{ chat: ChatHook }> = ({ chat }) => {
  const [input, setInput] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat.messages, chat.loading]);

  const validateMessage = (msg: string): string | null => {
    const trimmed = msg.trim();
    if (!trimmed) {
      return "Please enter a message";
    }
    if (trimmed.length > 5000) {
      return "Message must be 5000 characters or less";
    }
    return null;
  };

  async function handleSend() {
    const text = input.trim();
    setValidationError(null);

    const error = validateMessage(text);
    if (error) {
      setValidationError(error);
      return;
    }

    await chat.sendMessage(text);
    setInput("");
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!chat.loading) handleSend();
    }
  };

  return (
    <section className="chat-panel">
      <div className="chat-header">
        <Bot size={20} style={{ color: "var(--color-primary)" }} />
        <h3>AI Assistant</h3>
      </div>

      <div className="chat-messages">
        {(Array.isArray(chat.messages) ? chat.messages : []).map((m, i) => (
          <div key={i} className={`chat-msg chat-${m.role}`}>
            <div className={`chat-avatar ${m.role === "user" ? "user-avatar" : "ai-avatar"}`}>
              {m.role === "user" ? <User size={16} /> : <Sparkles size={16} />}
            </div>
            <div className="chat-bubble">
              {m.role === "assistant" ? (
                <MarkdownRenderer content={m.content} />
              ) : (
                m.content
              )}
            </div>
          </div>
        ))}

        {chat.loading && (
          <div className="typing-indicator">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {chat.error && (
        <div style={{ padding: "0 var(--space-lg)", color: "var(--color-error)", fontSize: "0.875rem" }}>
          {chat.error}
        </div>
      )}

      {validationError && (
        <div style={{ padding: "0 var(--space-lg)", color: "var(--color-error)", fontSize: "0.875rem" }}>
          {validationError}
        </div>
      )}

      <div className="chat-input-row">
        <div className="chat-input-wrapper">
          <input
            value={input}
            placeholder="Ask anything about this product..."
            onChange={(e) => {
              setInput(e.target.value);
              if (validationError) setValidationError(null);
            }}
            onKeyDown={handleKeyDown}
            disabled={chat.loading}
            aria-invalid={!!validationError}
            autoComplete="off"
          />
          <button
            className="chat-send-btn"
            onClick={handleSend}
            disabled={chat.loading || !input.trim()}
            title="Send message"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </section>
  );
};

export default ChatPanel;
