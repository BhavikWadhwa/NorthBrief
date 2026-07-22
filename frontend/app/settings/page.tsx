"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { getPreferences, updatePreferences } from "@/lib/api";
import { PreferencePayload } from "@/lib/types";
import { citiesByProvince, interestCategories, provinceOptions } from "@/lib/preferences-data";

export default function SettingsPage() {
  const router = useRouter();
  const { data, status } = useSession();
  const [payload, setPayload] = useState<PreferencePayload | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const cityOptions = payload?.province ? citiesByProvince[payload.province] ?? [] : [];

  useEffect(() => {
    if (!data?.accessToken) return;
    getPreferences(data.accessToken)
      .then((result) => {
        setError("");
        setPayload(result);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load settings."));
  }, [data?.accessToken]);

  if (status === "loading") return <div className="p-8">Loading...</div>;
  if (!data?.accessToken) {
    router.push("/signin");
    return null;
  }
  if (!payload) return <div className="p-8">Loading...</div>;

  return (
    <AppShell>
      <h1 className="font-display text-3xl">Settings</h1>
      <div className="mt-6 max-w-xl space-y-4 rounded-2xl border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900">
        <label className="text-sm">
          Province
          <select
            value={payload.province ?? ""}
            onChange={(event) =>
              setPayload((prev) =>
                prev
                  ? {
                      ...prev,
                      province: event.target.value || null,
                      city: null
                    }
                  : prev
              )
            }
            className="mt-1 h-11 w-full rounded-xl border border-zinc-300 bg-transparent px-3 dark:border-zinc-700"
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
          City
          <select
            value={payload.city ?? ""}
            disabled={!payload.province}
            onChange={(event) =>
              setPayload((prev) => (prev ? { ...prev, city: event.target.value || null } : prev))
            }
            className="mt-1 h-11 w-full rounded-xl border border-zinc-300 bg-transparent px-3 dark:border-zinc-700"
          >
            <option value="">None</option>
            {cityOptions.map((city) => (
              <option key={city.code} value={city.code}>
                {city.label}
              </option>
            ))}
          </select>
        </label>
        <div>
          <p className="mb-2 text-sm font-semibold">Interests</p>
          <div className="flex flex-wrap gap-2">
            {interestCategories.map((category) => {
              const selected = payload.category_codes.includes(category.code);
              return (
                <button
                  key={category.code}
                  type="button"
                  className={`rounded-full px-3 py-2 text-xs ${
                    selected
                      ? "bg-brand-600 text-white"
                      : "bg-zinc-200 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
                  }`}
                  onClick={() =>
                    setPayload((prev) =>
                      prev
                        ? {
                            ...prev,
                            category_codes: selected
                              ? prev.category_codes.filter((code) => code !== category.code)
                              : [...prev.category_codes, category.code]
                          }
                        : prev
                    )
                  }
                >
                  {category.label}
                </button>
              );
            })}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={payload.skip_personalization}
            onChange={(event) =>
              setPayload((prev) => (prev ? { ...prev, skip_personalization: event.target.checked } : prev))
            }
          />
          <span className="text-sm">Use Canada-wide default feed</span>
        </div>
        <Button
          disabled={saving}
          onClick={async () => {
            setSaving(true);
            setError("");
            setMessage("");
            try {
              await updatePreferences(data.accessToken, payload);
              setMessage("Settings saved.");
            } catch (err) {
              setError(err instanceof Error ? err.message : "Could not save settings.");
            }
            setSaving(false);
          }}
        >
          {saving ? "Saving..." : "Save settings"}
        </Button>
        {message ? <p className="text-sm text-brand-700 dark:text-brand-300">{message}</p> : null}
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
      </div>
    </AppShell>
  );
}
