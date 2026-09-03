"use client";

import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowLeft, Loader2, Sparkles, Wand2 } from "lucide-react";

import { useRequireAuth } from "@/hooks/use-require-auth";
import { useAiSeoSuggestions, useGenerateAIContent, useKeywordDensity, useSeoAudit } from "@/hooks/use-platform";
import { AnimatedButton } from "@/components/ui/animated-button";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { springs } from "@/lib/motion";

const RING_RADIUS = 54;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;

function gradeColor(grade: string): string {
  if (grade.startsWith("A")) return "#10b981";
  if (grade.startsWith("B")) return "#5b4ef9";
  if (grade.startsWith("C")) return "#f59e0b";
  return "#ef4444";
}

/** Animated 0-100 SEO score ring — the panel's signature real-time gauge, driven by whatever score the last audit/score call returned. */
function ScoreRing({ score, grade }: { score: number; grade: string }) {
  const color = gradeColor(grade);
  const offset = RING_CIRCUMFERENCE * (1 - score / 100);

  return (
    <div className="relative flex h-40 w-40 items-center justify-center">
      <svg width="160" height="160" viewBox="0 0 160 160" className="-rotate-90">
        <circle cx="80" cy="80" r={RING_RADIUS} fill="none" stroke="#e2e8f0" strokeWidth="12" />
        <motion.circle
          cx="80"
          cy="80"
          r={RING_RADIUS}
          fill="none"
          stroke={color}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={RING_CIRCUMFERENCE}
          initial={{ strokeDashoffset: RING_CIRCUMFERENCE }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <motion.span
          key={score}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={springs.bouncy}
          className="text-3xl font-bold text-slate-900"
        >
          {score}
        </motion.span>
        <span className="text-xs font-semibold uppercase tracking-widest" style={{ color }}>
          Grade {grade}
        </span>
      </div>
    </div>
  );
}

function AICopyGeneratorDrawer({
  onApply,
}: {
  onApply: (fields: { metaTitle?: string; metaDescription?: string }) => void;
}) {
  const [storeId, setStoreId] = useState("");
  const [contentType, setContentType] = useState("meta_description");
  const [instructions, setInstructions] = useState("");
  const generate = useGenerateAIContent();

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button className="bg-[#5b4ef9] hover:bg-[#4a3ee0]">
          <Wand2 className="h-4 w-4" />
          AI Copy Generator
        </Button>
      </SheetTrigger>
      <SheetContent className="w-full overflow-y-auto sm:max-w-md">
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-[#5b4ef9]" />
            AI Copy Generator
          </SheetTitle>
        </SheetHeader>

        <div className="flex flex-col gap-4 px-4 pb-6">
          <div>
            <Label htmlFor="ai-store-id">Store ID (UUID)</Label>
            <Input id="ai-store-id" value={storeId} onChange={(e) => setStoreId(e.target.value)} className="mt-1.5" />
          </div>
          <div>
            <Label htmlFor="ai-content-type">Content type</Label>
            <select
              id="ai-content-type"
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
              className="mt-1.5 w-full rounded-md border border-input bg-input-background px-3 py-2 text-sm"
            >
              <option value="page_title">Page title</option>
              <option value="meta_description">Meta description</option>
              <option value="blog_draft">Blog draft</option>
            </select>
          </div>
          <div>
            <Label htmlFor="ai-instructions">Instructions</Label>
            <Textarea
              id="ai-instructions"
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
              placeholder="e.g. Focus on handmade leather bags, warm and premium tone."
              className="mt-1.5 min-h-24"
            />
          </div>

          <AnimatedButton
            status={generate.isPending ? "pending" : generate.isSuccess ? "success" : generate.isError ? "error" : "idle"}
            label="Generate draft"
            loadingLabel="Generating..."
            icon={<Sparkles className="h-4 w-4" />}
            disabled={!storeId.trim()}
            className="w-full bg-[#5b4ef9] hover:bg-[#4a3ee0]"
            onClick={() => generate.mutate({ storeId: storeId.trim(), contentType, instructions: instructions || undefined })}
          />

          {generate.data && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4"
            >
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Generated draft</p>
              <p className="mt-2 whitespace-pre-wrap text-sm text-slate-700">
                {generate.data.content ?? "No content returned — check the Gemini API key is configured."}
              </p>
              {generate.data.content && (
                <Button
                  size="sm"
                  variant="outline"
                  className="mt-3"
                  onClick={() =>
                    onApply(
                      contentType === "page_title"
                        ? { metaTitle: generate.data!.content ?? undefined }
                        : { metaDescription: generate.data!.content ?? undefined },
                    )
                  }
                >
                  Apply to Storefront
                </Button>
              )}
            </motion.div>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
}

export default function SeoAiAssistantPage() {
  const { ready } = useRequireAuth();
  const [metaTitle, setMetaTitle] = useState("");
  const [metaDescription, setMetaDescription] = useState("");
  const [slug, setSlug] = useState("");
  const [content, setContent] = useState("");
  const [targetKeyword, setTargetKeyword] = useState("");

  const audit = useSeoAudit();
  const aiSuggestions = useAiSeoSuggestions();
  const keywordDensity = useKeywordDensity();

  if (!ready) return null;

  const score = audit.data?.seoScore ?? 0;
  const grade = audit.data?.grade ?? "—";

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#ffffff_0%,#f7f5ff_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">KarobarOne portal</p>
            <h1 className="mt-1 text-xl font-semibold text-slate-950">SEO & AI Assistant</h1>
          </div>
          <Link
            href="/platform-admin-portal"
            className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-[#5b4ef9]/30 hover:text-[#5b4ef9]"
          >
            <ArrowLeft className="size-4" />
            Dashboard
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-3xl font-semibold tracking-tight">SEO score & AI copy</h2>
            <p className="text-sm text-slate-500">Audit a page's metadata and generate AI-assisted copy for it.</p>
          </div>
          <AICopyGeneratorDrawer
            onApply={(fields) => {
              if (fields.metaTitle !== undefined) setMetaTitle(fields.metaTitle);
              if (fields.metaDescription !== undefined) setMetaDescription(fields.metaDescription);
            }}
          />
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_320px]">
          <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
            <h3 className="text-sm font-semibold text-slate-900">Page metadata</h3>
            <div className="mt-4 grid gap-4">
              <div>
                <Label htmlFor="meta-title">Meta title</Label>
                <Input id="meta-title" value={metaTitle} onChange={(e) => setMetaTitle(e.target.value)} className="mt-1.5" />
              </div>
              <div>
                <Label htmlFor="meta-description">Meta description</Label>
                <Textarea
                  id="meta-description"
                  value={metaDescription}
                  onChange={(e) => setMetaDescription(e.target.value)}
                  className="mt-1.5 min-h-20"
                />
              </div>
              <div>
                <Label htmlFor="slug">Slug</Label>
                <Input id="slug" value={slug} onChange={(e) => setSlug(e.target.value)} className="mt-1.5" placeholder="handmade-leather-bags" />
              </div>
              <div>
                <Label htmlFor="content">Page content</Label>
                <Textarea id="content" value={content} onChange={(e) => setContent(e.target.value)} className="mt-1.5 min-h-32" />
              </div>
            </div>

            <div className="mt-5 flex flex-wrap gap-3">
              <AnimatedButton
                status={audit.isPending ? "pending" : audit.isSuccess ? "success" : audit.isError ? "error" : "idle"}
                label="Run SEO audit"
                loadingLabel="Auditing..."
                icon={<Sparkles className="h-4 w-4" />}
                className="bg-[#5b4ef9] hover:bg-[#4a3ee0]"
                onClick={() => audit.mutate({ metaTitle, metaDescription, slug, content })}
              />
              <Button
                variant="outline"
                disabled={aiSuggestions.isPending}
                onClick={() => aiSuggestions.mutate({ metaTitle, metaDescription, content })}
              >
                {aiSuggestions.isPending && <Loader2 className="h-4 w-4 animate-spin" />}
                Get AI suggestions
              </Button>
            </div>

            {audit.data && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 grid gap-4 sm:grid-cols-2"
              >
                <div className="rounded-2xl border border-slate-100 bg-slate-50/60 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Issues</p>
                  {audit.data.issues.length === 0 ? (
                    <p className="mt-2 text-sm text-emerald-600">No issues found.</p>
                  ) : (
                    <ul className="mt-2 space-y-1 text-sm text-red-600">
                      {audit.data.issues.map((issue, i) => (
                        <li key={i}>{issue}</li>
                      ))}
                    </ul>
                  )}
                </div>
                <div className="rounded-2xl border border-slate-100 bg-slate-50/60 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Recommendations</p>
                  <ul className="mt-2 space-y-1 text-sm text-slate-600">
                    {audit.data.recommendations.map((rec, i) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </div>
                <div className="flex items-center gap-3 text-xs text-slate-500 sm:col-span-2">
                  <Badge variant="outline">Title {audit.data.titleLength} chars</Badge>
                  <Badge variant="outline">Description {audit.data.descriptionLength} chars</Badge>
                  <Badge variant="outline">{audit.data.wordCount} words</Badge>
                  <Badge variant="outline">Readability: {audit.data.readability}</Badge>
                </div>
              </motion.div>
            )}

            {aiSuggestions.data && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 rounded-2xl border border-[#5b4ef9]/20 bg-[#5b4ef9]/5 p-4"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#5b4ef9]">AI-suggested copy</p>
                <p className="mt-2 text-sm font-medium text-slate-800">{aiSuggestions.data.improvedTitle}</p>
                <p className="mt-1 text-sm text-slate-600">{aiSuggestions.data.improvedDescription}</p>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {aiSuggestions.data.keywords.map((kw) => (
                    <Badge key={kw} variant="secondary">
                      {kw}
                    </Badge>
                  ))}
                </div>
                <Button
                  size="sm"
                  variant="outline"
                  className="mt-3"
                  onClick={() => {
                    setMetaTitle(aiSuggestions.data!.improvedTitle);
                    setMetaDescription(aiSuggestions.data!.improvedDescription);
                  }}
                >
                  Apply to Storefront
                </Button>
              </motion.div>
            )}

            <div className="mt-6 border-t border-slate-100 pt-5">
              <p className="text-sm font-semibold text-slate-900">Keyword density</p>
              <div className="mt-3 flex flex-wrap items-end gap-3">
                <div>
                  <Label htmlFor="target-keyword">Target keyword</Label>
                  <Input
                    id="target-keyword"
                    value={targetKeyword}
                    onChange={(e) => setTargetKeyword(e.target.value)}
                    className="mt-1.5 w-56"
                  />
                </div>
                <Button
                  variant="outline"
                  disabled={!targetKeyword.trim() || !content.trim() || keywordDensity.isPending}
                  onClick={() => keywordDensity.mutate({ content, targetKeyword: targetKeyword.trim() })}
                >
                  {keywordDensity.isPending && <Loader2 className="h-4 w-4 animate-spin" />}
                  Analyze
                </Button>
              </div>
              {keywordDensity.data && (
                <p className="mt-3 text-sm text-slate-600">
                  <span className="font-medium text-slate-900">{keywordDensity.data.density.toFixed(2)}%</span> density ·{" "}
                  {keywordDensity.data.count} occurrences in {keywordDensity.data.totalWords} words —{" "}
                  <span className={keywordDensity.data.status === "optimal" ? "text-emerald-600" : "text-amber-600"}>
                    {keywordDensity.data.status}
                  </span>
                  . {keywordDensity.data.recommendation}
                </p>
              )}
            </div>
          </section>

          <aside className="flex flex-col items-center gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-slate-900">Live SEO score</p>
            <ScoreRing score={score} grade={grade} />
            <p className="text-center text-xs text-slate-400">
              Run an audit to update this score in real time as you edit metadata.
            </p>
          </aside>
        </div>
      </main>
    </div>
  );
}
