import { useState } from "react";
import { apiReview } from "../api/client";
import type { EnhancedProductReview } from "../api/types";

export function useReview() {
  const [review, setReview] = useState<EnhancedProductReview | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function fetchReview(
    productName: string,
    dataMode: "web" | "ai" | "hybrid" = "web",
    userId?: string,
  ): Promise<EnhancedProductReview | null> {
    setLoading(true);
    setError(null);
    try {
      const data = await apiReview(productName, dataMode, userId);
      setReview(data);
      return data;
    } catch (e: any) {
      const message = e?.message ?? "Failed to fetch review";
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  }

  function setReviewData(value: EnhancedProductReview | null) {
    setReview(value);
  }

  return { review, loading, error, fetchReview, setReviewData };
}
