export type Song = {
  id: number;
  title: string;
  artist: string;
  genre: string;
  mood: string;
  energy: number;
  tempo_bpm?: number;
  valence?: number;
  danceability?: number;
  acousticness?: number;
};

export type Recommendation = {
  rank: number;
  song: Song;
  score: number;
  reasons: string[];
  explanation: string;
};

export type Confidence = {
  label: string;
  score: number;
  reasons: string[];
};

export type Guardrails = {
  safe: boolean;
  requires_human_review?: boolean;
  warnings?: string[];
};

export type TraceStep = {
  step: string;
  status: string;
};

export type Intent = {
  favorite_genre?: string;
  favorite_mood?: string;
  target_energy?: number;
  matched_terms?: unknown;
  warnings?: string[];
  [key: string]: unknown;
};

export type ApiResponse = {
  prompt: string;
  intent: Intent;
  recommendations: Recommendation[];
  confidence: Confidence;
  guardrails: Guardrails;
  trace: TraceStep[];
};
