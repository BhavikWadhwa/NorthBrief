"use client";

import Link from "next/link";

import { AppShell } from "@/components/app-shell";

const categories = ["Local", "Canada", "World", "Finance", "Trending", "Politics", "Humanitarian", "Wholesome"];

export default function CategoryPage() {
  return (
    <AppShell>
      <h1 className="font-display text-3xl">Categories</h1>
      <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">Jump to your preferred stream quickly.</p>
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {categories.map((item) => (
          <Link
            key={item}
            href={`/feed?tab=${item.toLowerCase().replaceAll(" ", "_")}`}
            className="rounded-xl border border-zinc-200 bg-white p-4 transition hover:border-brand-500 dark:border-zinc-800 dark:bg-zinc-900"
          >
            {item}
          </Link>
        ))}
      </div>
    </AppShell>
  );
}

