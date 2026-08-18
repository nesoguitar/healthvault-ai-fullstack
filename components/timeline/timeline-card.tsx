import { MedicalEvent } from "@/types";
import { eventTypeConfig } from "@/lib/config";
import { formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

export function TimelineCard({ event, isLast }: { event: MedicalEvent; isLast?: boolean }) {
  const cfg = eventTypeConfig[event.type];
  const Icon = cfg.icon;

  return (
    <div className="relative flex gap-4 pb-8 last:pb-0">
      {!isLast && <span className="absolute left-5 top-11 h-[calc(100%-1.75rem)] w-px bg-border" />}
      <span className={`relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${cfg.bg}`}>
        <Icon className={`h-4.5 w-4.5 ${cfg.color}`} />
      </span>
      <div className="min-w-0 flex-1 rounded-xl border border-border bg-card p-4 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <Badge variant="outline" className={cfg.color}>{cfg.label}</Badge>
          <span className="text-xs text-muted-foreground">{formatDate(event.date)}</span>
        </div>
        <h4 className="mt-2 text-sm font-semibold">{event.title}</h4>
        <p className="mt-1 text-sm text-muted-foreground">{event.description}</p>
        {(event.provider || event.facility) && (
          <p className="mt-2 text-xs text-muted-foreground/80">
            {event.provider}
            {event.provider && event.facility ? " · " : ""}
            {event.facility}
          </p>
        )}
      </div>
    </div>
  );
}
