"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { addSource, getAdminArticles, listSources, triggerIngestion, updateSource } from "@/lib/api";
import { AdminArticle, SourceItem } from "@/lib/types";

export default function AdminPage() {
  const router = useRouter();
  const { data, status } = useSession();
  const [articles, setArticles] = useState<AdminArticle[]>([]);
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [creatingSource, setCreatingSource] = useState(false);
  const [form, setForm] = useState({
    name: "",
    source_type: "rss",
    feed_url: "",
    site_url: "",
    default_region_code: "ca",
    default_category_code: "canada",
    priority: 0.8,
    is_active: true
  });

  async function refresh() {
    if (!data?.accessToken) return;
    try {
      setError("");
      const result = await getAdminArticles(data.accessToken);
      setArticles(result.items);
      const sourceRows = await listSources(data.accessToken);
      setSources(sourceRows);
    } catch (err) {
      setArticles([]);
      setSources([]);
      setError(err instanceof Error ? err.message : "Could not load admin articles.");
    }
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data?.accessToken]);

  if (status === "loading") return <div className="p-8">Loading...</div>;
  if (!data?.accessToken) {
    router.push("/signin");
    return null;
  }

  return (
    <AppShell>
      <h1 className="font-display text-3xl">Developer dashboard</h1>
      <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
        Trigger ingestion runs and inspect processing quality.
      </p>
      <div className="mt-4 flex gap-3">
        <Button
          disabled={running}
          onClick={async () => {
            setRunning(true);
            setMessage("");
            setError("");
            try {
              const result = await triggerIngestion(data.accessToken);
              setMessage(`Run ${result.run_id} completed: ${result.inserted_count} inserted.`);
              await refresh();
            } catch (err) {
              setError(err instanceof Error ? err.message : "Ingestion failed.");
            }
            setRunning(false);
          }}
        >
          {running ? "Running..." : "Run ingestion now"}
        </Button>
        <Button variant="ghost" onClick={refresh}>
          Refresh list
        </Button>
      </div>
      {message ? <p className="mt-3 text-sm text-brand-700 dark:text-brand-300">{message}</p> : null}
      {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
      <div className="mt-5 overflow-x-auto rounded-xl border border-zinc-200 dark:border-zinc-800">
        <table className="w-full text-left text-sm">
          <thead className="bg-zinc-100 dark:bg-zinc-900">
            <tr>
              <th className="px-3 py-2">Headline</th>
              <th className="px-3 py-2">Summary</th>
              <th className="px-3 py-2">Category conf.</th>
              <th className="px-3 py-2">Region conf.</th>
            </tr>
          </thead>
          <tbody>
            {articles.map((item) => (
              <tr key={item.processed_article_id} className="border-t border-zinc-200 dark:border-zinc-800">
                <td className="px-3 py-2">{item.headline}</td>
                <td className="px-3 py-2">{item.summary_status}</td>
                <td className="px-3 py-2">{item.category_confidence.toFixed(2)}</td>
                <td className="px-3 py-2">{item.region_confidence.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 rounded-xl border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="font-display text-2xl">Sources</h2>
        <p className="mt-1 text-sm text-zinc-500">Manage active feeds, priorities, and defaults.</p>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-100 dark:bg-zinc-900">
              <tr>
                <th className="px-3 py-2">Source</th>
                <th className="px-3 py-2">Region</th>
                <th className="px-3 py-2">Category</th>
                <th className="px-3 py-2">Priority</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {sources.map((source) => (
                <tr key={source.id} className="border-t border-zinc-200 dark:border-zinc-800">
                  <td className="px-3 py-2">
                    <p>{source.name}</p>
                    <p className="text-xs text-zinc-500">{source.feed_url}</p>
                  </td>
                  <td className="px-3 py-2">{source.default_region_code || "-"}</td>
                  <td className="px-3 py-2">{source.default_category_code || "-"}</td>
                  <td className="px-3 py-2">{source.priority.toFixed(2)}</td>
                  <td className="px-3 py-2">{source.is_active ? "active" : "disabled"}</td>
                  <td className="px-3 py-2">
                    <button
                      className="rounded border border-zinc-300 px-2 py-1 text-xs dark:border-zinc-700"
                      onClick={async () => {
                        if (!data?.accessToken) return;
                        try {
                          await updateSource(data.accessToken, source.id, { is_active: !source.is_active });
                          await refresh();
                        } catch (err) {
                          setError(err instanceof Error ? err.message : "Could not update source.");
                        }
                      }}
                    >
                      {source.is_active ? "Disable" : "Enable"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-8 rounded-xl border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="font-display text-2xl">Add Source</h2>
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          <input
            className="h-10 rounded border border-zinc-300 bg-transparent px-3 text-sm dark:border-zinc-700"
            placeholder="Source name"
            value={form.name}
            onChange={(event) => setForm((prev) => ({ ...prev, name: event.target.value }))}
          />
          <input
            className="h-10 rounded border border-zinc-300 bg-transparent px-3 text-sm dark:border-zinc-700"
            placeholder="Feed URL"
            value={form.feed_url}
            onChange={(event) => setForm((prev) => ({ ...prev, feed_url: event.target.value }))}
          />
          <input
            className="h-10 rounded border border-zinc-300 bg-transparent px-3 text-sm dark:border-zinc-700"
            placeholder="Site URL"
            value={form.site_url}
            onChange={(event) => setForm((prev) => ({ ...prev, site_url: event.target.value }))}
          />
          <input
            className="h-10 rounded border border-zinc-300 bg-transparent px-3 text-sm dark:border-zinc-700"
            placeholder="Region code (ca-bc, global...)"
            value={form.default_region_code}
            onChange={(event) => setForm((prev) => ({ ...prev, default_region_code: event.target.value }))}
          />
          <input
            className="h-10 rounded border border-zinc-300 bg-transparent px-3 text-sm dark:border-zinc-700"
            placeholder="Category code (local, canada...)"
            value={form.default_category_code}
            onChange={(event) => setForm((prev) => ({ ...prev, default_category_code: event.target.value }))}
          />
          <input
            className="h-10 rounded border border-zinc-300 bg-transparent px-3 text-sm dark:border-zinc-700"
            type="number"
            min={0}
            max={1}
            step={0.01}
            placeholder="Priority"
            value={form.priority}
            onChange={(event) => setForm((prev) => ({ ...prev, priority: Number(event.target.value) }))}
          />
        </div>
        <div className="mt-4">
          <Button
            disabled={creatingSource}
            onClick={async () => {
              if (!data?.accessToken) return;
              setCreatingSource(true);
              try {
                await addSource(data.accessToken, {
                  ...form,
                  site_url: form.site_url || undefined,
                  default_region_code: form.default_region_code || undefined,
                  default_category_code: form.default_category_code || undefined
                });
                setMessage(`Source ${form.name} added.`);
                setForm({
                  name: "",
                  source_type: "rss",
                  feed_url: "",
                  site_url: "",
                  default_region_code: "ca",
                  default_category_code: "canada",
                  priority: 0.8,
                  is_active: true
                });
                await refresh();
              } catch (err) {
                setError(err instanceof Error ? err.message : "Could not create source.");
              } finally {
                setCreatingSource(false);
              }
            }}
          >
            {creatingSource ? "Adding..." : "Add source"}
          </Button>
        </div>
      </div>
    </AppShell>
  );
}
