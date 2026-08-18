import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { labFlagConfig } from "@/lib/config";
import { formatDate } from "@/lib/utils";
import { FlaskConical } from "lucide-react";
import { LabResult } from "@/types";

export function LabsCard({ labs }: { labs: LabResult[] }) {
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-base">Recent Labs</CardTitle>
        <FlaskConical className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent className="space-y-3">
        {labs.length === 0 ? (
          <p className="text-sm text-muted-foreground">No lab results on record yet.</p>
        ) : (
          labs.map((l) => {
            const cfg = labFlagConfig[l.flag];
            return (
              <div key={l.id} className="flex items-center justify-between gap-2">
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium">{l.testName}</p>
                  <p className="text-xs text-muted-foreground">
                    {l.value} {l.unit} · {formatDate(l.date)}
                  </p>
                </div>
                <Badge variant={cfg.badgeVariant}>{cfg.label}</Badge>
              </div>
            );
          })
        )}
      </CardContent>
    </Card>
  );
}
