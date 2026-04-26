"use client";

import { useState } from "react";
import { PromptBox } from "../components/PromptBox";
import { Results } from "../components/Results";

type ApiResponse = Record<string, unknown> | null;

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<ApiResponse>(null);
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

      const data = await response.json();

      if (!response.ok) {
        throw new Error(JSON.stringify(data));
      }

      setResult(data);
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
    <main className="page">
      <section className="shell" aria-labelledby="page-title">
        <div className="intro">
          <p className="eyebrow">VibeMatch AI</p>
          <h1 id="page-title">Generate a playlist from a vibe.</h1>
          <p>
            Type a mood, moment, or listening goal, then call the local FastAPI
            backend.
          </p>
        </div>

        <PromptBox
          prompt={prompt}
          isLoading={isLoading}
          onPromptChange={setPrompt}
          onGenerate={handleGenerate}
        />

        <Results result={result} error={error} isLoading={isLoading} />
      </section>
    </main>
  );
}

