import React, { useEffect, useState } from "react";
import { useReview } from "../hooks/useReview";
import { useChat } from "../hooks/useChat";
import { useAuth } from "../auth/AuthContext";
import SearchBar from "../components/SearchBar";
import DecisionCard from "../components/DecisionCard";
import PricingSection from "../components/PricingSection";
import ProsConsSection from "../components/ProsConsSection";
import SentimentSection from "../components/SentimentSection";
import RiskSection from "../components/RiskSection";
import TimingSection from "../components/TimingSection";
import BestForSection from "../components/BestForSection";
import AlternativesSection from "../components/AlternativesSection";
import SourcesSection from "../components/SourcesSection";
import ChatPanel from "../components/ChatPanel";
import HistorySidebar, { HistoryEntry } from "../components/HistorySidebar";
import GlobalAlert from "../components/GlobalAlert";
import ProfilePanel, { UserProfile } from "../components/ProfilePanel";
import ComparisonView from "../components/ComparisonView";
import FakeSpotterPanel from "../components/FakeSpotterPanel";
import NetPricePanel from "../components/NetPricePanel";
import ReliabilityPanel from "../components/ReliabilityPanel";
import ResalePanel from "../components/ResalePanel";
import SmartSwapPanel from "../components/SmartSwapPanel";
import VideoProof from "../components/VideoProof";
import VoxPopuliPanel from "../components/VoxPopuliPanel";
import WhatIfPanel from "../components/WhatIfPanel";
import AnalysisProgress from "../components/AnalysisProgress";
import { fetchHistorySummary, fetchLatestSession } from "../api/history";
import { getUserId } from "../api/userId";
import { apiGetProfile } from "../api/client";
import { fetchChatSession } from "../api/chatHistory";
import { fetchSavedReview } from "../api/reviewHistory";
import { addToShortlist, fetchShortlist, removeFromShortlist } from "../api/shortlist";
import type { ChatMessage } from "../api/client";

const ReviewPage: React.FC = () => {
  const [productName, setProductName] = useState("");
  const [dataMode, setDataMode] = useState<"web" | "ai" | "hybrid">("web");
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [shortlist, setShortlist] = useState<HistoryEntry[]>([]);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const [conversationHistory, setConversationHistory] = useState<ChatMessage[]>([]);
  const [uiMessage, setUiMessage] = useState<string | null>(null);
  const [showCompare, setShowCompare] = useState(false);
  const [comparisonProducts, setComparisonProducts] = useState<string[]>([]);

  const { token } = useAuth();
  const { review, loading, error, fetchReview, setReviewData } = useReview();
  const [sessionId, setSessionId] = useState<number | null>(null);
  const chat = useChat(productName, dataMode, userProfile, {
    sessionId,
    initialHistory: conversationHistory,
    userId: userId ?? undefined,
  });

  function isUnauthorized(err: unknown): boolean {
    const msg = err instanceof Error ? err.message : String(err);
    return msg.includes("401") || msg.toLowerCase().includes("unauthorized");
  }

  function normalizeProductName(name: string): string {
    return name.trim().toLowerCase().replace(/\s+/g, " ");
  }

  async function loadHistoryAndShortlist() {
    try {
      const data = await fetchHistorySummary(userId ?? undefined);
      const entries: HistoryEntry[] = (data.products ?? []).map((p) => ({
        name: p.product_name,
        rating: p.rating ?? undefined,
        price: p.price ?? undefined,
        timestamp: p.last_viewed_at,
      }));
      setHistory(entries);
    } catch (e) {
      if (isUnauthorized(e)) {
        setUiMessage("Log in to save and view your history and shortlist.");
      }
    }

    try {
      const items = await fetchShortlist();
      setShortlist(items.map((i) => ({ name: i.product_name, timestamp: i.created_at })));
    } catch (e) {
      if (isUnauthorized(e)) {
        setUiMessage("Log in to save and view your history and shortlist.");
      }
    }
  }

  useEffect(() => {
    // Get stable userId for guest flows
    const id = getUserId();
    setUserId(id);
    (async () => {
      try {
        const apiProfile = await apiGetProfile();
        if (apiProfile) setUserProfile(apiProfile);
      } catch {
        // ignore
      }
    })();
    // Refresh user data when token changes (login/logout/session refresh)
    if (!token) {
      setHistory([]);
      setShortlist([]);
    }
    loadHistoryAndShortlist();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  async function handleAnalyze(name: string) {
    const trimmed = name.trim();
    if (!trimmed) return;

    // Scroll to top immediately
    window.scrollTo(0, 0);

    // Intelligent Comparison Detection
    // Regex for: "compare A vs B", "A vs B", "A and B", "A, B"
    const compareRegex = /(?:^compare\s+)?(.+?)\s+(?:vs\.?|versus|and|,)\s+(.+)/i;
    const match = trimmed.match(compareRegex);

    if (match) {
      // Likely a comparison intent
      // Check if it's "compare X" where X might be a single product name vs implicit
      // But for now assume explicit comparison if separator exists

      // Extract potential names
      // If query is "compare A and B and C", simple regex might be tricky
      // Let's use a simpler splitter strategy if "compare" keyword or "vs" is present

      const isExplicitCompare = /^compare\s+/i.test(trimmed) || /\s+vs\.?\s+/i.test(trimmed);
      const hasSeparator = /\s+(?:and|,)\s+/i.test(trimmed);

      if (isExplicitCompare || (hasSeparator && trimmed.split(/\s+(?:and|,)\s+/).length >= 2)) {
        const cleanName = trimmed.replace(/^compare\s+/i, "");
        const products = cleanName.split(/\s+(?:vs\.?|versus|and|,)\s+/i)
          .map(p => p.trim())
          .filter(p => p.length > 0);

        if (products.length >= 2) {
          // Switch to comparison mode
          setComparisonProducts(products.slice(0, 3)); // Max 3
          setShowCompare(true);
          return;
        }
      }
    }

    // Clear previous review and reset state for new search
    setReviewData(null);
    setSessionId(null);
    setConversationHistory([]);
    setProductName(trimmed);
    setComparisonProducts([]); // Reset auto-comparison
    setShowCompare(false); // Switch back to review mode if not comparison

    const result = await fetchReview(trimmed, dataMode, userId ?? undefined);
    if (result) {
      // Scroll to top AFTER result renders - use setTimeout to ensure DOM updates first
      setTimeout(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 100);

      const entry: HistoryEntry = {
        name: result.product_name,
        rating: result.predicted_rating,
        price: result.price_naira ?? result.price_info,
        timestamp: new Date().toISOString(),
      };
      setHistory((prev) => [...prev, entry]);
    }
  }

  async function handleSelectHistory(entry: HistoryEntry) {
    setProductName(entry.name);

    // Restore saved review first (so the UI populates immediately)
    try {
      const saved = await fetchSavedReview(entry.name);
      if (saved) {
        setReviewData(saved);
      }
    } catch {
      // ignore
    }

    // Restore latest chat session for that product
    try {
      const latestSessionId = await fetchLatestSession(userId ?? undefined, entry.name);

      if (!latestSessionId) {
        setSessionId(null);
        setConversationHistory([]);
        return;
      }

      const messages = await fetchChatSession(userId ?? undefined, latestSessionId);
      setSessionId(latestSessionId);
      setConversationHistory(
        messages.map((m) => ({ role: m.role, content: m.content })),
      );
    } catch {
      setSessionId(null);
      setConversationHistory([]);
    }
  }

  async function handleShortlistAdd(entry: HistoryEntry) {
    // Avoid duplicate adds locally too (case/space insensitive)
    const target = normalizeProductName(entry.name);
    if (shortlist.some((p) => normalizeProductName(p.name) === target)) return;

    try {
      await addToShortlist(entry.name);
      setShortlist((prev) => [...prev, entry]);
    } catch (e) {
      if (isUnauthorized(e)) {
        setUiMessage("Please log in to add items to your shortlist.");
      } else {
        setUiMessage("Failed to add to shortlist. Please try again.");
      }
    }
  }

  async function handleShortlistRemove(entry: HistoryEntry) {
    try {
      await removeFromShortlist(entry.name);
      const target = normalizeProductName(entry.name);
      setShortlist((prev) => prev.filter((p) => normalizeProductName(p.name) !== target));
    } catch (e) {
      if (isUnauthorized(e)) {
        setUiMessage("Please log in to manage your shortlist.");
      } else {
        setUiMessage("Failed to remove from shortlist. Please try again.");
      }
    }
  }

  // Adapter to ensure backward compatibility with components expecting 'expert_assessment'
  const displayReview = review ? {
    ...review,
    expert_assessment: review.expert_assessment || review.summary || "No assessment available."
  } : null;

  return (
    <div className="layout">
      <aside className="sidebar">
        <ProfilePanel value={userProfile} onChange={setUserProfile} userId={userId ?? undefined} />
        <HistorySidebar
          history={history}
          shortlist={shortlist}
          onSelectHistory={handleSelectHistory}
          onRemoveShortlist={handleShortlistRemove}
        />
        {/* Compare button in sidebar */}
        <button
          className={`sidebar-compare-btn ${showCompare ? 'active' : ''}`}
          onClick={() => {
            setShowCompare(!showCompare);
            if (!showCompare) window.scrollTo({ top: 0, behavior: 'smooth' });
          }}
        >
          ⚖️ {showCompare ? 'Hide Comparison' : 'Compare Products'}
        </button>
      </aside>
      <main className="content">
        <SearchBar
          onAnalyze={handleAnalyze}
          dataMode={dataMode}
          setDataMode={setDataMode}
        />

        {/* Content Mode Tabs */}
        <div className="content-mode-tabs">
          <button
            className={`mode-tab ${!showCompare ? 'active' : ''}`}
            onClick={() => setShowCompare(false)}
          >
            🔍 Review
          </button>
          <button
            className={`mode-tab ${showCompare ? 'active' : ''}`}
            onClick={() => {
              setShowCompare(true);
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }}
          >
            ⚖️ Compare
          </button>
        </div>

        <GlobalAlert message={uiMessage} onClose={() => setUiMessage(null)} />
        <GlobalAlert message={error} />
        {loading && !review && (
          <AnalysisProgress isLoading={loading} productName={productName || "product"} />
        )}
        {review && displayReview && (
          <>
            <DecisionCard
              review={displayReview}
              onShortlistAdd={handleShortlistAdd}
              isShortlisted={shortlist.some(
                (p) => normalizeProductName(p.name) === normalizeProductName(displayReview.product_name),
              )}
            />
            <PricingSection review={displayReview} />
            <ProsConsSection review={displayReview} />
            <SentimentSection review={displayReview} />

            {/* Advanced Intelligence Grid */}
            <div className="intelligence-grid">
              {displayReview.net_price_report && (
                <div className="grid-net-price">
                  <NetPricePanel review={displayReview} />
                </div>
              )}

              {displayReview.reliability_report && (
                <div className="grid-reliability">
                  <ReliabilityPanel review={displayReview} />
                </div>
              )}

              {displayReview.smart_swap_report && (
                <div className="grid-smart-swap">
                  <SmartSwapPanel review={displayReview} />
                </div>
              )}

              {displayReview.fake_spotter_report && (
                <div className="grid-fake-spotter">
                  <FakeSpotterPanel review={displayReview} />
                </div>
              )}

              {displayReview.resale_analysis && (
                <div className="grid-resale">
                  <ResalePanel review={displayReview} />
                </div>
              )}

              {displayReview.what_if_report && (
                <div className="grid-what-if">
                  <WhatIfPanel review={displayReview} />
                </div>
              )}

              {displayReview.video_proof && (
                <div className="grid-video">
                  <VideoProof review={displayReview} />
                </div>
              )}

              {displayReview.vox_populi_report && (
                <div className="grid-vox">
                  <VoxPopuliPanel review={displayReview} />
                </div>
              )}
            </div>

            <RiskSection review={displayReview} />
            <TimingSection review={displayReview} />
            <BestForSection review={displayReview} />
            <AlternativesSection review={displayReview} />
            <SourcesSection review={displayReview} />
            <ChatPanel chat={chat} />
          </>
        )}

        {/* Compare Mode Content */}
        {showCompare && <ComparisonView shortlist={shortlist} prefillNames={comparisonProducts} />}
      </main>
    </div>
  );
};

export default ReviewPage;
