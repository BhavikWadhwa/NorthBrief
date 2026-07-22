"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";

import { getPreferences, updatePreferences } from "@/lib/api";
import { PreferencePayload } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { citiesByProvince, interestCategories, provinceOptions } from "@/lib/preferences-data";

export default function OnboardingPage() {
  const router = useRouter();
  const { data, status } = useSession();
  const [payload, setPayload] = useState<PreferencePayload>({
    country: "Canada",
    province: "bc",
    city: "vancouver",
    category_codes: ["local", "canada"],
    local_global_weight: 0.7,
    finance_weight: 0.4,
    skip_personalization: false
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const cityOptions = payload.province ? citiesByProvince[payload.province] ?? [] : [];

  useEffect(() => {
    if (!data?.accessToken) return;
    getPreferences(data.accessToken)
      .then((result) => {
        setError("");
        setPayload(result);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load preferences."));
  }, [data?.accessToken]);

  if (status === "loading") return <div className="p-8">Loading...</div>;
  if (!data?.accessToken) {
    router.push("/signin");
    return null;
  }

  async function saveAndContinue(skip = false) {
    setSaving(true);
    setError("");
    try {
      await updatePreferences(data.accessToken, { ...payload, skip_personalization: skip });
      router.push("/feed");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save onboarding preferences.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="font-display text-3xl">Set up your briefing</h1>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
        Choose your region and interests. You can change everything later in settings.
      </p>

      <section className="mt-6 grid gap-4 rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900">
        <label className="text-sm">
          Province
          <select
            className="mt-2 h-11 w-full rounded-xl border border-zinc-300 bg-transparent px-3 dark:border-zinc-700"
            value={payload.province ?? ""}
            onChange={(event) =>
              setPayload((prev) => ({
                ...prev,
                province: event.target.value || null,
                city: null
              }))
            }
          >
            <option value="">None</option>
            {provinceOptions.map((province) => (
              <option key={province.code} value={province.code}>
                {province.label}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          City / Metro
          <select
            className="mt-2 h-11 w-full rounded-xl border border-zinc-300 bg-transparent px-3 dark:border-zinc-700"
            value={payload.city ?? ""}
            disabled={!payload.province}
            onChange={(event) => setPayload((prev) => ({ ...prev, city: event.target.value || null }))}
          >
            <option value="">None</option>
            {cityOptions.map((city) => (
              <option key={city.code} value={city.code}>
                {city.label}
              </option>
            ))}
          </select>
        </label>
      </section>

      <section className="mt-4 rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900">
        <p className="mb-3 text-sm font-semibold">Interests</p>
        <div className="flex flex-wrap gap-2">
          {interestCategories.map((category) => {
            const selected = payload.category_codes.includes(category.code);
            return (
              <button
                key={category.code}
                className={`rounded-full px-3 py-2 text-xs ${
                  selected
                    ? "bg-brand-600 text-white"
                    : "bg-zinc-200 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
                }`}
                onClick={() =>
                  setPayload((prev) => ({
                    ...prev,
                    category_codes: selected
                      ? prev.category_codes.filter((code) => code !== category.code)
                      : [...prev.category_codes, category.code]
                  }))
                }
              >
                {category.label}
              </button>
            );
          })}
        </div>
      </section>

      <div className="mt-5 flex gap-3">
        <Button disabled={saving} onClick={() => saveAndContinue(false)}>
          Save preferences
        </Button>
        <Button disabled={saving} onClick={() => saveAndContinue(true)} variant="ghost">
          Skip personalization
        </Button>
      </div>
      {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
    </div>
  );
}
