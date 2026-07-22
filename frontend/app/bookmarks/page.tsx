"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";

import { AppShell } from "@/components/app-shell";
import { NewsCard } from "@/components/news-card-v2";
import { deleteBookmark, getBookmarks } from "@/lib/api";
import { FeedItem } from "@/lib/types";

export default function BookmarksPage() {
  const router = useRouter();
  const { data, status } = useSession();
  const [items, setItems] = useState<FeedItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!data?.accessToken) return;
    setLoading(true);
    getBookmarks(data.accessToken)
      .then((result) => {
        setError("");
        setItems(result.items);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load bookmarks."))
      .finally(() => setLoading(false));
  }, [data?.accessToken]);

  if (status === "loading") return <div className="p-8">Loading...</div>;
  if (!data?.accessToken) {
    router.push("/signin");
    return null;
  }

  return (
    <AppShell>
      <h1 className="font-display text-3xl">Saved stories</h1>
      <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">Your bookmarks are private and account-based.</p>
      {loading ? <p className="mt-4">Loading...</p> : null}
      {error ? <p className="mt-4 text-sm text-red-600">{error}</p> : null}
      {!loading && !items.length ? <p className="mt-4 text-sm text-zinc-500">No saved stories yet.</p> : null}
      <div className="mt-5 grid gap-4 md:grid-cols-2">
        {items.map((item) => (
          <div key={item.id}>
            <NewsCard item={item} />
            <button
              onClick={() => {
                deleteBookmark(data.accessToken, item.id)
                  .then(() => setItems((current) => current.filter((entry) => entry.id !== item.id)))
                  .catch((err) => setError(err instanceof Error ? err.message : "Could not remove bookmark."));
              }}
              className="mt-2 text-xs text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
            >
              Remove bookmark
            </button>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
