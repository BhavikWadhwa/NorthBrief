import { AdminArticle, FeedResponse, IngestionRunResponse, PreferencePayload, SourceItem } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function apiFetch<T>(path: string, token: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(init?.headers || {})
    },
    cache: "no-store"
  });
  if (!response.ok) {
    let message = `API request failed with status ${response.status}`;
    try {
      const payload = await response.json();
      if (typeof payload?.detail === "string") {
        message = payload.detail;
      }
    } catch {
      const fallback = await response.text().catch(() => "");
      if (fallback) {
        message = fallback;
      }
    }
    throw new Error(message);
  }
  if (response.status === 204) {
    return null as T;
  }
  return response.json();
}

export async function getFeed(token: string, tab: string): Promise<FeedResponse> {
  return apiFetch<FeedResponse>(`/feed?tab=${tab}`, token);
}

export async function getBookmarks(token: string): Promise<FeedResponse> {
  return apiFetch<FeedResponse>("/bookmarks", token);
}

export async function createBookmark(token: string, processedArticleId: string) {
  return apiFetch("/bookmarks", token, {
    method: "POST",
    body: JSON.stringify({ processed_article_id: processedArticleId })
  });
}

export async function deleteBookmark(token: string, processedArticleId: string) {
  return apiFetch(`/bookmarks/${processedArticleId}`, token, { method: "DELETE" });
}

export async function getPreferences(token: string): Promise<PreferencePayload> {
  return apiFetch<PreferencePayload>("/preferences", token);
}

export async function updatePreferences(token: string, payload: PreferencePayload): Promise<PreferencePayload> {
  return apiFetch<PreferencePayload>("/preferences", token, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export async function triggerIngestion(token: string) {
  return apiFetch<IngestionRunResponse>("/admin/ingestion/run", token, { method: "POST" });
}

export async function getAdminArticles(token: string) {
  return apiFetch<{ items: AdminArticle[] }>("/admin/articles", token);
}

export async function listSources(token: string): Promise<SourceItem[]> {
  return apiFetch<SourceItem[]>("/sources", token);
}

export async function addSource(
  token: string,
  payload: {
    name: string;
    source_type: string;
    feed_url: string;
    site_url?: string;
    default_region_code?: string;
    default_category_code?: string;
    priority: number;
    is_active: boolean;
  }
): Promise<SourceItem> {
  return apiFetch<SourceItem>("/sources", token, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function updateSource(
  token: string,
  sourceId: string,
  payload: { is_active?: boolean; priority?: number; default_region_code?: string; default_category_code?: string }
): Promise<SourceItem> {
  return apiFetch<SourceItem>(`/sources/${sourceId}`, token, {
    method: "PATCH",
    body: JSON.stringify(payload)
  });
}
