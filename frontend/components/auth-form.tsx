"use client";

import { FormEvent, useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function AuthForm({ mode }: { mode: "signin" | "signup" }) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const form = new FormData(event.currentTarget);
      const email = String(form.get("email") || "");
      const password = String(form.get("password") || "");
      const displayName = String(form.get("displayName") || "").trim();

      if (mode === "signup") {
        const signupResponse = await fetch(`${apiBaseUrl}/auth/signup`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email,
            password,
            display_name: displayName || email.split("@")[0]
          })
        });
        if (!signupResponse.ok) {
          const payload = await signupResponse.json().catch(() => ({}));
          const detail = typeof payload?.detail === "string" ? payload.detail : null;
          setError(detail || "Could not create account. Please try a different email.");
          return;
        }
      }

      const result = await signIn("credentials", {
        redirect: false,
        email,
        password
      });
      if (result?.error || !result?.ok) {
        setError(
          mode === "signup"
            ? "Account created, but sign-in failed. Please sign in manually."
            : "Could not sign in. Please check details and try again."
        );
        return;
      }
      router.push("/onboarding");
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-950">
      <h1 className="font-display text-2xl">{mode === "signup" ? "Create account" : "Welcome back"}</h1>
      {mode === "signup" ? <Input name="displayName" placeholder="Display name" required /> : null}
      <Input name="email" type="email" placeholder="you@domain.com" required />
      <Input name="password" type="password" placeholder="Password" required minLength={8} />
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      <Button disabled={loading} className="w-full" type="submit">
        {loading ? "Please wait..." : mode === "signup" ? "Create and continue" : "Sign in"}
      </Button>
    </form>
  );
}
