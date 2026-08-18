"use client";

import { AppShell } from "@/components/navigation/app-shell";
import { Timeline } from "@/components/timeline/timeline";
import { Skeleton } from "@/components/ui/skeleton";
import { useTimeline } from "@/hooks/use-timeline";
import { AlertCircle } from "lucide-react";

export default function TimelinePage() {
  const { data: events, isLoading, isError, error } = useTimeline();

  return (
    <AppShell title="Health Timeline">
      <div className="mb-6 max-w-2xl">
        <h2 className="text-2xl font-semibold tracking-tight">Your health timeline</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Every visit, result, and procedure, organized chronologically
          {events ? ` across ${events.length} events.` : "."}
        </p>
      </div>

      <div className="max-w-3xl">
        {isLoading && (
          <div className="space-y-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={i} className="h-28 rounded-xl" />
            ))}
          </div>
        )}

        {isError && (
          <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-16 text-center">
            <AlertCircle className="h-8 w-8 text-destructive/60" />
            <p className="mt-3 text-sm font-medium">Couldn't load your timeline</p>
            <p className="mt-1 max-w-sm text-xs text-muted-foreground">
              {error instanceof Error ? error.message : "Please check that the API is running and try again."}
            </p>
          </div>
        )}

        {events && <Timeline events={events} />}
      </div>
    </AppShell>
  );
}
