export interface SentimentScore {
  overall_sentiment: string;
  polarity_score: number;
  subjectivity_score: number;
  compound_score: number;
  positive_ratio: number;
  negative_ratio: number;
  neutral_ratio: number;
  sentiment_confidence: number;
  emotional_tone: string;
  key_positive_aspects: string[];
  key_negative_aspects: string[];
}

export interface AspectBreakdownItem {
  aspect: string;
  mentions: number;
  avg_sentiment: number;
}

export interface ProductImage {
  url: string;
  thumbnail_url?: string;
  source: string;
  width?: number;
  height?: number;
  alt_text?: string;
}

export interface RetailerPrice {
  retailer_id: string;
  retailer_name: string;
  price_naira?: number;
  original_price?: number;
  discount_percent?: number;
  product_url: string;
  in_stock: boolean;
  last_checked: string;
}

export interface PriceComparison {
  product_name: string;
  prices: RetailerPrice[];
  lowest_price?: number;
  highest_price?: number;
  average_price?: number;
  best_deal_retailer?: string;
  price_last_updated: string;
  currency: string;
  deal_quality?: string | null;
  deal_explanation?: string | null;
}

export interface RedFlag {
  severity: "high" | "medium" | "low";
  category: string;
  title: string;
  description: string;
  affected_percentage?: number;
}

export interface RedFlagReport {
  product_name: string;
  red_flags: RedFlag[];
  overall_risk_level: "high" | "medium" | "low";
  risk_score: number;
  fake_review_score?: number;
  common_complaints: string[];
  recommendation: string;
}

export interface PurchaseTimingAdvice {
  product_name: string;
  lifecycle_stage: string;
  recommendation: "buy_now" | "wait" | "consider_alternatives";
  reasoning: string;
  new_model_expected: boolean;
  expected_release_window?: string | null;
  best_sale_periods: string[];
  current_deal_quality: string;
  price_trend: string;
  confidence: number;
}

export interface BestForTag {
  use_case: string;
  score: number;
  reasoning: string;
}

export interface AlternativeProduct {
  product_name: string;
  url: string;
  snippet: string;
  reason: string;
}

export interface ReliabilityRisk {
  risk_type: string;
  likelihood: string;
  description: string;
  prevention_tip: string;
}

export interface RepairEstimate {
  part_name: string;
  estimated_cost_naira: string;
  availability_in_nigeria: string;
}

export interface ReliabilityReport {
  overall_reliability_score: number;
  predicted_lifespan: string;
  common_risks: ReliabilityRisk[];
  repair_costs: RepairEstimate[];
  warranty_difficulty: string;
}

export interface ResaleAnalysis {
  predicted_value_1yr: string;
  predicted_value_3yr: string;
  depreciation_rate: string;
  investment_score: number;
  verdict: string;
}

export interface VideoMoment {
  label: string;
  search_query: string;
  youtube_url: string;
  description: string;
}

export interface VideoProof {
  moments: VideoMoment[];
}

export interface AuthenticityCheck {
  check_type: string;
  instruction: string;
  expected_result: string;
  warning_sign: string;
}

export interface FakeSpotterReport {
  risk_level: string;
  common_scams: string[];
  verification_steps: AuthenticityCheck[];
}

export interface ForumOpinion {
  platform: string;
  sentiment: string;
  key_takeaway: string;
}

export interface VoxPopuliReport {
  owner_verdict: string;
  love_it_for: string[];
  hate_it_for: string[];
  forum_consensus: ForumOpinion[];
}

export interface SmartSwapOption {
  product_name: string;
  price: number;
  condition: string;
  performance_diff: string;
  camera_diff: string;
  reason_to_buy: string;
  reason_to_avoid: string;
}

export interface SmartSwapReport {
  base_price: number;
  recommendation: string;
  swaps: SmartSwapOption[];
}

export interface DisasterScenario {
  name: string;
  scenario: string;
  outcome: string;
  repair_cost_estimate: string;
  survivability_score: number;
}

export interface WhatIfReport {
  disaster_score: number;
  scenarios: DisasterScenario[];
}

export interface TradeInOption {
  device_name: string;
  estimated_value: number;
  net_price: number;
}

export interface NetPriceReport {
  upgrade_from: TradeInOption[];
}

export interface EnhancedProductReview {
  product_name: string;
  specifications_inferred: string;
  predicted_rating: string;
  pros: string[];
  cons: string[];
  summary: string;
  expert_assessment?: string; // Back-compat for Outer components
  price_info: string;
  sources: string[];
  last_updated: string;
  data_source_type: string;

  sentiment_analysis?: SentimentScore;
  product_images: ProductImage[];
  primary_image_url?: string | null;

  pros_sentiment?: number;
  cons_sentiment?: number;
  summary_sentiment?: number;
  aspect_breakdown?: AspectBreakdownItem[];

  price_comparison?: PriceComparison;
  price_naira?: number;
  original_price_display?: string | null;
  price_confidence?: string;

  red_flag_report?: RedFlagReport;
  timing_advice?: PurchaseTimingAdvice;
  reliability_report?: ReliabilityReport;

  resale_analysis?: ResaleAnalysis;
  video_proof?: VideoProof;
  fake_spotter_report?: FakeSpotterReport;
  vox_populi_report?: VoxPopuliReport;
  smart_swap_report?: SmartSwapReport;
  what_if_report?: WhatIfReport;
  net_price_report?: NetPriceReport;

  best_for_tags?: BestForTag[];
  budget_tier?: string;

  data_quality?: string;
  alternatives?: AlternativeProduct[];
}

export interface ProductComparisonItem {
  product_name: string;
  price_naira?: number;
  rating?: string;
  pros: string[];
  cons: string[];
  image_url?: string;
  best_for: string[];
  value_score?: number;
}

export interface ProductComparison {
  products: ProductComparisonItem[];
  comparison_categories: string[];
  winner_by_category: Record<string, string>;
  overall_winner?: string | null;
  best_value?: string | null;
  best_budget?: string | null;
  best_premium?: string | null;
  ai_recommendation: string;
  comparison_date: string;
}
