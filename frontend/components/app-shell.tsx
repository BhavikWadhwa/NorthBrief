"use client";

import Link from "next/link";
import { signOut, useSession } from "next-auth/react";
import { Moon, Sun } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useTheme } from "@/components/theme-provider";

export function AppShell({ children }: { children: React.ReactNode }) {
  const { data } = useSession();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-gradient-to-b from-brand-50 via-zinc-50 to-white text-zinc-900 dark:from-zinc-950 dark:via-zinc-950 dark:to-black dark:text-zinc-100">
      <header className="sticky top-0 z-30 border-b border-zinc-200/60 bg-white/85 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/85">
        <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-4 py-3">
          <Link href="/feed" className="font-display text-xl font-semibold tracking-tight">
            NorthBrief
          </Link>
          <nav className="hidden items-center gap-3 text-sm md:flex">
            <Link href="/feed">Feed</Link>
            <Link href="/bookmarks">Saved</Link>
            <Link href="/settings">Settings</Link>
            <Link href="/admin">Admin</Link>
          </nav>
          <div className="flex items-center gap-2">
            <Button variant="ghost" onClick={toggleTheme} aria-label="Toggle theme">
              {theme === "light" ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
            </Button>
            {data?.user ? (
              <Button variant="ghost" onClick={() => signOut({ callbackUrl: "/signin" })}>
                Sign out
              </Button>
            ) : null}
          </div>
        </div>
      </header>
      <main className="mx-auto w-full max-w-5xl px-4 py-6">{children}</main>
    </div>
  );
}

