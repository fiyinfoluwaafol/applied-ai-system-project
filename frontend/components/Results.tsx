type ResultsProps = {
  result: Record<string, unknown> | null;
  error: string;
  isLoading: boolean;
};

export function Results({ result, error, isLoading }: ResultsProps) {
  return (
    <section className="results" aria-live="polite">
      <h2>Results</h2>
      {isLoading && <p>Calling backend...</p>}
      {error && <pre className="error">{error}</pre>}
      {!isLoading && !error && !result && (
        <p className="muted">Backend response will appear here.</p>
      )}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </section>
  );
}

