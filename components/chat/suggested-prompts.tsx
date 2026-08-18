import { Sparkles } from "lucide-react";
import { suggestedPrompts } from "@/mock-data/chat";

export function SuggestedPrompts({ onSelect }: { onSelect: (prompt: string) => void }) {
  return (
    <div className="grid gap-2 sm:grid-cols-2">
      {suggestedPrompts.map((p) => (
        <button
          key={p}
          onClick={() => onSelect(p)}
          className="flex items-start gap-2 rounded-xl border border-border bg-card p-3.5 text-left text-sm transition-colors hover:border-primary hover:bg-primary/5"
        >
          <Sparkles className="mt-0.5 h-3.5 w-3.5 shrink-0 text-teal" />
          {p}
        </button>
      ))}
    </div>
  );
}
