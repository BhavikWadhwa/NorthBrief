export type FeedTab = "for-you" | "local" | "canada" | "world" | "finance" | "trending";

export interface FeedItem {
  id: string;
  headline: string;
  summary: string;
  why_this_matters: string;
  key_impact?: string | null;
  category: string;
  region?: string | null;
  source_name: string;
  source_domain?: string | null;
  published_at?: string | null;
  canonical_url: string;
  image_url?: string | null;
  rank_score: number;
}

export interface FeedResponse {
  items: FeedItem[];
  total: number;
}

export interface PreferencePayload {
  country: string;
  province?: string | null;
  city?: string | null;
  category_codes: string[];
  local_global_weight: number;
  finance_weight: number;
  skip_personalization: boolean;
}

export interface SourceItem {
  id: string;
  name: string;
  feed_url: string;
  site_url?: string | null;
  source_type: string;
  default_region_code?: string | null;
  default_category_code?: string | null;
  priority: number;
  is_active: boolean;
  last_fetched_at?: string | null;
  last_status?: string | null;
  failure_count: number;
}

export interface AdminArticle {
  processed_article_id: string;
  raw_article_id: string;
  headline: string;
  summary_status: string;
  quality_flags: string[];
  category_confidence: number;
  region_confidence: number;
}

export interface IngestionRunResponse {
  run_id: string;
  status: string;
  fetched_count: number;
  inserted_count: number;
  deduped_count: number;
  error_count: number;
}
