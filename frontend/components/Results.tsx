"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  Brain,
  CheckCircle2,
  Circle,
  Gauge,
  Headphones,
  Loader2,
  Music2,
  Radio,
  Search,
  ShieldCheck,
  Sparkles,
  WandSparkles,
} from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { ApiResponse, Recommendation, TraceStep } from "@/lib/types";

type ResultsProps = {
  result: ApiResponse | null;
  error: string;
  isLoading: boolean;
};

type TraceDisplayState = "pending" | "active" | "complete" | "error";

const expectedTraceSteps = [
  {
    step: "intent_parser",
    label: "Intent",
    description: "Reading genre, mood, and energy cues.",
    icon: Brain,
  },
  {
    step: "retriever",
    label: "Catalog",
    description: "Opening the local song library.",
    icon: Search,
  },
  {
    step: "scorer",
    label: "Scoring",
    description: "Ranking tracks against the prompt.",
    icon: Activity,
  },
  {
    step: "explainer",
    label: "Explain",
    description: "Writing recommendation reasons.",
    icon: WandSparkles,
  },
  {
    step: "confidence",
    label: "Confidence",
    description: "Checking strength of the match.",
    icon: Gauge,
  },
  {
    step: "guardrails",
    label: "Guardrails",
    description: "Reviewing the final playlist.",
    icon: ShieldCheck,
  },
];

function formatPercent(value?: number) {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return "0%";
  }

  return `${Math.round(Math.max(0, Math.min(1, value)) * 100)}%`;
}

function formatScore(value: number) {
  return value.toFixed(2);
}

function formatMatchScore(value: number) {
  return `${Math.round(Math.max(0, Math.min(1, value / 4)) * 100)}%`;
}

function titleCase(value: string) {
  return value
    .replace(/[_-]/g, " ")
    .replace(/\w\S*/g, (word) => word.charAt(0).toUpperCase() + word.slice(1));
}

function stringifyIntentValue(value: unknown) {
  if (value === null || value === undefined || value === "") {
    return "None";
  }

  if (Array.isArray(value)) {
    return value.length ? value.join(", ") : "None";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

function getTraceState(
  index: number,
  visibleStepCount: number,
  isLoading: boolean,
  actualTrace?: TraceStep
): TraceDisplayState {
  if (actualTrace) {
    return actualTrace.status === "ok" ? "complete" : "error";
  }

  if (!isLoading) {
    return "pending";
  }

  if (index < visibleStepCount - 1) {
    return "complete";
  }

  if (index === visibleStepCount - 1) {
    return "active";
  }

  return "pending";
}

function TraceStatusIcon({ state }: { state: TraceDisplayState }) {
  if (state === "complete") {
    return <CheckCircle2 className="size-4 text-emerald-300" aria-hidden="true" />;
  }

  if (state === "error") {
    return <AlertTriangle className="size-4 text-rose-300" aria-hidden="true" />;
  }

  if (state === "active") {
    return <Loader2 className="size-4 animate-spin text-primary" aria-hidden="true" />;
  }

  return <Circle className="size-4 text-muted-foreground" aria-hidden="true" />;
}

function TracePanel({
  trace,
  isLoading,
}: {
  trace?: TraceStep[];
  isLoading: boolean;
}) {
  const [visibleStepCount, setVisibleStepCount] = useState(0);

  useEffect(() => {
    if (!isLoading) {
      setVisibleStepCount(trace?.length ? expectedTraceSteps.length : 0);
      return;
    }

    setVisibleStepCount(1);
    const timer = window.setInterval(() => {
      setVisibleStepCount((current) =>
        Math.min(expectedTraceSteps.length, current + 1)
      );
    }, 620);

    return () => window.clearInterval(timer);
  }, [isLoading, trace?.length]);

  const traceByStep = useMemo(() => {
    return new Map((trace ?? []).map((item) => [item.step, item]));
  }, [trace]);

  return (
    <Card className="overflow-hidden">
      <CardHeader className="border-b border-border/60 bg-white/[0.03]">
        <div className="flex items-center justify-between gap-3">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Radio className="size-5 text-primary" aria-hidden="true" />
              Agent trace
            </CardTitle>
            <CardDescription>Live run state from the curator pipeline.</CardDescription>
          </div>
          <Badge variant={isLoading ? "default" : trace?.length ? "success" : "muted"}>
            {isLoading ? "Running" : trace?.length ? "Complete" : "Idle"}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="grid gap-3 pt-5">
        {expectedTraceSteps.map((item, index) => {
          const actualTrace = traceByStep.get(item.step);
          const state = getTraceState(
            index,
            visibleStepCount,
            isLoading,
            actualTrace
          );
          const StepIcon = item.icon;

          return (
            <div
              key={item.step}
              className={cn(
                "flex items-start gap-3 rounded-lg border p-3 transition-all",
                state === "active" &&
                  "border-primary/50 bg-primary/10 shadow-glow",
                state === "complete" &&
                  "border-emerald-400/20 bg-emerald-400/[0.06]",
                state === "error" && "border-rose-400/30 bg-rose-400/[0.08]",
                state === "pending" && "border-border/50 bg-muted/30 opacity-65"
              )}
            >
              <div className="mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-lg border border-border/70 bg-background/60">
                <StepIcon className="size-4 text-muted-foreground" aria-hidden="true" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="text-sm font-semibold text-foreground">{item.label}</p>
                  <Badge
                    variant={
                      state === "complete"
                        ? "success"
                        : state === "error"
                          ? "warning"
                          : state === "active"
                            ? "default"
                            : "muted"
                    }
                  >
                    {actualTrace?.status ?? state}
                  </Badge>
                </div>
                <p className="mt-1 text-sm leading-5 text-muted-foreground">
                  {item.description}
                </p>
              </div>
              <TraceStatusIcon state={state} />
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}

function InsightCard({
  icon: Icon,
  label,
  value,
  detail,
}: {
  icon: typeof Sparkles;
  label: string;
  value: string;
  detail?: string;
}) {
  return (
    <Card className="bg-card/65">
      <CardContent className="flex gap-3 p-4">
        <div className="flex size-10 shrink-0 items-center justify-center rounded-lg border border-primary/20 bg-primary/10 text-primary">
          <Icon className="size-4" aria-hidden="true" />
        </div>
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase text-muted-foreground">
            {label}
          </p>
          <p className="mt-1 truncate text-lg font-semibold text-foreground">
            {value}
          </p>
          {detail && (
            <p className="mt-1 line-clamp-2 text-sm leading-5 text-muted-foreground">
              {detail}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function RecommendationCard({
  recommendation,
}: {
  recommendation: Recommendation;
}) {
  const { song } = recommendation;

  return (
    <Card className="group overflow-hidden transition-transform hover:-translate-y-0.5 hover:border-primary/35 hover:shadow-glow">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex min-w-0 items-start gap-4">
            <div className="flex size-12 shrink-0 items-center justify-center rounded-lg border border-primary/25 bg-gradient-to-br from-primary/20 to-accent/20 text-primary">
              <span className="text-sm font-bold">#{recommendation.rank}</span>
            </div>
            <div className="min-w-0">
              <h3 className="truncate text-lg font-semibold text-foreground">
                {song.title}
              </h3>
              <p className="mt-1 truncate text-sm text-muted-foreground">
                {song.artist}
              </p>
            </div>
          </div>
          <Badge variant="outline">{formatMatchScore(recommendation.score)}</Badge>
        </div>

        <div className="mt-5 grid grid-cols-3 gap-2">
          <Badge variant="secondary" className="justify-center truncate">
            {song.genre}
          </Badge>
          <Badge variant="secondary" className="justify-center truncate">
            {song.mood}
          </Badge>
          <Badge variant="secondary" className="justify-center truncate">
            {song.tempo_bpm ?? "--"} bpm
          </Badge>
        </div>

        <div className="mt-5 rounded-lg border border-border/60 bg-background/45 p-4">
          <p className="text-sm leading-6 text-muted-foreground">
            {recommendation.explanation}
          </p>
        </div>

        <div className="mt-4 flex flex-wrap gap-2">
          {recommendation.reasons.map((reason) => (
            <Badge key={reason} variant="muted">
              {reason}
            </Badge>
          ))}
        </div>

        <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-gradient-to-r from-primary to-accent"
            style={{ width: formatMatchScore(recommendation.score) }}
          />
        </div>
        <p className="mt-2 text-xs text-muted-foreground">
          Match score {formatScore(recommendation.score)}
        </p>
      </CardContent>
    </Card>
  );
}

function EmptyState() {
  return (
    <Card className="min-h-[280px]">
      <CardContent className="flex h-full min-h-[280px] flex-col items-center justify-center p-8 text-center">
        <div className="mb-5 flex size-14 items-center justify-center rounded-lg border border-primary/20 bg-primary/10 text-primary shadow-glow">
          <Headphones className="size-6" aria-hidden="true" />
        </div>
        <h2 className="text-2xl font-semibold text-foreground">
          Your playlist will settle here.
        </h2>
        <p className="mt-3 max-w-md text-sm leading-6 text-muted-foreground">
          Recommendations, confidence, guardrails, and the agent trace will
          appear as one clean run.
        </p>
      </CardContent>
    </Card>
  );
}

export function Results({ result, error, isLoading }: ResultsProps) {
  const intentEntries = result
    ? Object.entries(result.intent).filter(([, value]) => value !== undefined)
    : [];

  return (
    <section className="grid gap-6" aria-live="polite">
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="size-4" aria-hidden="true" />
          <AlertTitle>Request failed</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {!result && !isLoading && !error && <EmptyState />}

      {(isLoading || result) && (
        <>
          <TracePanel trace={result?.trace} isLoading={isLoading} />

          {result && (
            <>
              <div className="grid gap-3 sm:grid-cols-3">
                <InsightCard
                  icon={Gauge}
                  label="Confidence"
                  value={`${titleCase(result.confidence.label)} ${formatPercent(
                    result.confidence.score
                  )}`}
                  detail={result.confidence.reasons.join(", ")}
                />
                <InsightCard
                  icon={Music2}
                  label="Intent"
                  value={[
                    result.intent.favorite_genre,
                    result.intent.favorite_mood,
                  ]
                    .filter(Boolean)
                    .join(" / ") || "Broad match"}
                  detail={
                    typeof result.intent.target_energy === "number"
                      ? `Target energy ${formatPercent(result.intent.target_energy)}`
                      : undefined
                  }
                />
                <InsightCard
                  icon={ShieldCheck}
                  label="Guardrails"
                  value={result.guardrails.safe ? "Safe" : "Review"}
                  detail={
                    result.guardrails.warnings?.length
                      ? result.guardrails.warnings.join(", ")
                      : "No warnings returned"
                  }
                />
              </div>

              {intentEntries.length > 0 && (
                <Card className="bg-card/60">
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center gap-2 text-base">
                      <Sparkles className="size-4 text-primary" aria-hidden="true" />
                      Parsed intent
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="flex flex-wrap gap-2">
                    {intentEntries.map(([key, value]) => (
                      <Badge key={key} variant="outline" className="max-w-full gap-1">
                        <span className="text-muted-foreground">{titleCase(key)}:</span>
                        <span className="truncate">{stringifyIntentValue(value)}</span>
                      </Badge>
                    ))}
                  </CardContent>
                </Card>
              )}

              <div>
                <div className="mb-4 flex items-end justify-between gap-4">
                  <div>
                    <h2 className="text-2xl font-semibold text-foreground">
                      Recommended tracks
                    </h2>
                    <p className="mt-1 text-sm text-muted-foreground">
                      Curated from the local catalog for "{result.prompt}".
                    </p>
                  </div>
                  <Badge variant="secondary">
                    {result.recommendations.length} tracks
                  </Badge>
                </div>
                <div className="grid gap-4 xl:grid-cols-2">
                  {result.recommendations.map((recommendation) => (
                    <RecommendationCard
                      key={`${recommendation.rank}-${recommendation.song.id}`}
                      recommendation={recommendation}
                    />
                  ))}
                </div>
              </div>
            </>
          )}
        </>
      )}
    </section>
  );
}
