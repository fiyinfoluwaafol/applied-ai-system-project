"use client";

import { useState } from "react";
import { PromptBox } from "../components/PromptBox";
import { Results } from "../components/Results";
import type { ApiResponse } from "@/lib/types";

function getApiErrorMessage(payload: unknown) {
  if (payload && typeof payload === "object" && "detail" in payload) {
    const detail = (payload as { detail: unknown }).detail;
    return typeof detail === "string" ? detail : JSON.stringify(detail);
  }

  return "Unable to generate a playlist from the current prompt.";
}

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleGenerate() {
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      const data: unknown = await response.json();

      if (!response.ok) {
        throw new Error(getApiErrorMessage(data));
      }

      setResult(data as ApiResponse);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to reach the backend."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="relative min-h-screen overflow-hidden px-4 py-6 text-foreground sm:px-6 lg:px-8">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/70 to-transparent" />
      <section
        className="relative mx-auto flex w-full max-w-7xl flex-col gap-8"
        aria-labelledby="page-title"
      >
        <div className="flex flex-col gap-6 pt-8 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p className="mb-3 text-sm font-semibold uppercase text-primary">
              VibeMatch AI
            </p>
            <h1
              id="page-title"
              className="text-balance text-4xl font-semibold leading-tight tracking-normal text-foreground sm:text-5xl lg:text-6xl"
            >
              Generate a playlist from a vibe.
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
              A local music curator agent turns mood, genre, and energy cues
              into explainable recommendations.
            </p>
          </div>
          <div className="rounded-full border border-border/70 bg-card/60 px-4 py-2 text-sm text-muted-foreground shadow-glow backdrop-blur-xl">
            FastAPI-backed curator
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-[minmax(320px,0.82fr)_minmax(0,1.18fr)] lg:items-start">
          <PromptBox
            prompt={prompt}
            isLoading={isLoading}
            onPromptChange={setPrompt}
            onGenerate={handleGenerate}
          />

          <Results result={result} error={error} isLoading={isLoading} />
        </div>
      </section>
    </main>
  );
}
