"use client";

import { ExternalLink, BookmarkPlus } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

import { FeedItem } from "@/lib/types";
import { Button } from "@/components/ui/button";

interface NewsCardProps {
  item: FeedItem;
  onBookmark?: (id: string) => void;
}

export function NewsCard({ item, onBookmark }: NewsCardProps) {
  const published =
    item.published_at && !Number.isNaN(new Date(item.published_at).valueOf())
      ? formatDistanceToNow(new Date(item.published_at), { addSuffix: true })
      : "Recently";

  return (
    <article className="animate-fade-up rounded-2xl border border-zinc-200 bg-white/90 p-5 shadow-sm transition hover:shadow-md dark:border-zinc-800 dark:bg-zinc-900/80">
      <div className="mb-3 flex items-center justify-between text-xs">
        <span className="rounded-full bg-brand-100 px-2 py-1 font-medium text-brand-800 dark:bg-brand-800/40 dark:text-brand-100">
          {item.category}
        </span>
        <span className="text-zinc-500">{published}</span>
      </div>
      <h3 className="font-display text-xl leading-tight text-zinc-900 dark:text-zinc-100">{item.headline}</h3>
      <p className="mt-3 text-sm text-zinc-700 dark:text-zinc-300">{item.summary}</p>
      <p className="mt-3 rounded-lg bg-zinc-100 px-3 py-2 text-sm text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
        <strong>Why this matters:</strong> {item.why_this_matters}
      </p>
      {item.key_impact ? (
        <p className="mt-2 text-xs text-zinc-600 dark:text-zinc-400">
          <strong>Impact:</strong> {item.key_impact}
        </p>
      ) : null}
      <div className="mt-4 flex items-center justify-between text-xs text-zinc-500">
        <span>
          {item.source_name}
          {item.region ? ` • ${item.region}` : ""}
        </span>
        <span>{item.source_domain}</span>
      </div>
      <div className="mt-4 flex items-center gap-2">
        <a href={item.canonical_url} target="_blank" rel="noreferrer" className="w-full">
          <Button className="w-full" variant="secondary">
            Read full story <ExternalLink className="ml-2 h-4 w-4" />
          </Button>
        </a>
        {onBookmark ? (
          <Button variant="ghost" onClick={() => onBookmark(item.id)} aria-label="Bookmark">
            <BookmarkPlus className="h-4 w-4" />
          </Button>
        ) : null}
      </div>
    </article>
  );
}

