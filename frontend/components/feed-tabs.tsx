"use client";

import { FeedTab } from "@/lib/types";

const tabs: Array<{ key: FeedTab; label: string }> = [
  { key: "for-you", label: "For You" },
  { key: "local", label: "Local" },
  { key: "canada", label: "Canada" },
  { key: "world", label: "World" },
  { key: "finance", label: "Finance" },
  { key: "trending", label: "Trending" }
];

export function FeedTabs({ activeTab, onChange }: { activeTab: FeedTab; onChange: (tab: FeedTab) => void }) {
  return (
    <div className="no-scrollbar flex gap-2 overflow-x-auto pb-1">
      {tabs.map((tab) => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={`rounded-full px-4 py-2 text-sm transition ${
            activeTab === tab.key
              ? "bg-brand-600 text-white"
              : "bg-zinc-200 text-zinc-700 hover:bg-zinc-300 dark:bg-zinc-800 dark:text-zinc-200"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

