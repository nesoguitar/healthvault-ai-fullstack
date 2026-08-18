"use client";

import { useMemo, useState } from "react";
import { MedicalEvent, MedicalEventType } from "@/types";
import { TimelineCard } from "./timeline-card";
import { eventTypeConfig } from "@/lib/config";
import { cn } from "@/lib/utils";
import { History } from "lucide-react";

export function Timeline({ events }: { events: MedicalEvent[] }) {
  const [filter, setFilter] = useState<MedicalEventType | "all">("all");

  const sorted = useMemo(
    () => [...events].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()),
    [events]
  );

  const filtered = filter === "all" ? sorted : sorted.filter((e) => e.type === filter);

  return (
    <div>
      <div className="mb-6 flex flex-wrap gap-2">
        <button
          onClick={() => setFilter("all")}
          className={cn(
            "rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
            filter === "all" ? "border-primary bg-primary/10 text-primary" : "border-border text-muted-foreground hover:bg-muted"
          )}
        >
          All events
        </button>
        {(Object.keys(eventTypeConfig) as MedicalEventType[]).map((type) => (
          <button
            key={type}
            onClick={() => setFilter(type)}
            className={cn(
              "rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
              filter === type ? "border-primary bg-primary/10 text-primary" : "border-border text-muted-foreground hover:bg-muted"
            )}
          >
            {eventTypeConfig[type].label}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-16 text-center">
          <History className="h-8 w-8 text-muted-foreground/40" />
          <p className="mt-3 text-sm font-medium">No events of this type</p>
          <p className="mt-1 text-xs text-muted-foreground">Try a different filter or upload more records.</p>
        </div>
      ) : (
        <div>
          {filtered.map((event, i) => (
            <TimelineCard key={event.id} event={event} isLast={i === filtered.length - 1} />
          ))}
        </div>
      )}
    </div>
  );
}
