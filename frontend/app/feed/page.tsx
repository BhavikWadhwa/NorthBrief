"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";

import { AppShell } from "@/components/app-shell";
import { FeedTabs } from "@/components/feed-tabs";
import { NewsCard } from "@/components/news-card-v2";
import { Button } from "@/components/ui/button";
import { createBookmark, getFeed } from "@/lib/api";
import { FeedItem, FeedTab } from "@/lib/types";

function FeedContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { data, status } = useSession();
  const [tab, setTab] = useState<FeedTab>("for-you");
  const [items, setItems] = useState<FeedItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const requested = searchParams.get("tab") as FeedTab | null;
    if (requested && ["for-you", "local", "canada", "world", "finance", "trending"].includes(requested)) {
      setTab(requested);
    }
  }, [searchParams]);

  useEffect(() => {
    if (!data?.accessToken) return;
    setLoading(true);
    setError(null);
    getFeed(data.accessToken, tab)
      .then((result) => setItems(result.items))
      .catch(() => setError("Could not load feed right now."))
      .finally(() => setLoading(false));
  }, [data?.accessToken, tab]);

  if (status === "loading") return <div className="p-8">Loading...</div>;
  if (!data?.accessToken) {
    router.push("/signin");
    return null;
  }

  return (
    <AppShell>
      <div className="space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-display text-3xl">Your briefing</h1>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">Region-aware summaries with source links.</p>
          </div>
          <Button variant="ghost" onClick={() => router.push("/onboarding")}>
            Edit preferences
          </Button>
        </div>

        <FeedTabs activeTab={tab} onChange={setTab} />

        {loading ? <p>Loading stories...</p> : null}
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        {!loading && !items.length ? (
          <div className="rounded-2xl border border-dashed border-zinc-300 p-8 text-center text-sm text-zinc-600 dark:border-zinc-700 dark:text-zinc-300">
            No stories found for this filter yet.
          </div>
        ) : null}

        <div className="grid gap-4 md:grid-cols-2">
          {items.map((item) => (
            <NewsCard
              key={item.id}
              item={item}
              onBookmark={async (id) => {
                try {
                  await createBookmark(data.accessToken, id);
                } catch {
                  setError("Could not save this story right now.");
                }
              }}
            />
          ))}
        </div>
      </div>
    </AppShell>
  );
}

export default function FeedPage() {
  return (
    <Suspense fallback={<div className="p-8">Loading your briefing...</div>}>
      <FeedContent />
    </Suspense>
  );
}
