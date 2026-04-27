import { Loader2, Music2, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

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
    <Card className="overflow-hidden">
      <CardHeader className="border-b border-border/60 bg-white/[0.03]">
        <div className="mb-2 flex size-11 items-center justify-center rounded-lg border border-primary/20 bg-primary/10 text-primary shadow-glow">
          <Music2 className="size-5" aria-hidden="true" />
        </div>
        <CardTitle>Playlist prompt</CardTitle>
        <CardDescription>
          Mood, setting, genre, activity, or energy all work.
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <form
          className="flex flex-col gap-4"
          onSubmit={(event) => {
            event.preventDefault();
            onGenerate();
          }}
        >
          <label htmlFor="prompt" className="text-sm font-medium text-foreground">
            Vibe
          </label>
          <Textarea
            id="prompt"
            value={prompt}
            onChange={(event) => onPromptChange(event.target.value)}
            placeholder="happy pop songs for a sunny walk"
            rows={6}
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading} className="w-full sm:w-fit">
            {isLoading ? (
              <>
                <Loader2 className="animate-spin" aria-hidden="true" />
                Generating
              </>
            ) : (
              <>
                <Sparkles aria-hidden="true" />
                Generate playlist
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
