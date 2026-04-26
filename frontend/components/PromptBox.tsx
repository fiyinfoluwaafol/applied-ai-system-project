type PromptBoxProps = {
  prompt: string;
  isLoading: boolean;
  onPromptChange: (value: string) => void;
  onGenerate: () => void;
};

export function PromptBox({
  prompt,
  isLoading,
  onPromptChange,
  onGenerate,
}: PromptBoxProps) {
  return (
    <div className="promptBox">
      <label htmlFor="prompt">Prompt</label>
      <textarea
        id="prompt"
        value={prompt}
        onChange={(event) => onPromptChange(event.target.value)}
        placeholder="happy pop songs for a sunny walk"
        rows={4}
      />
      <button type="button" onClick={onGenerate} disabled={isLoading}>
        {isLoading ? "Generating..." : "Generate playlist"}
      </button>
    </div>
  );
}

