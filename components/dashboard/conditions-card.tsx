import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { diagnosisStatusConfig } from "@/lib/config";
import { Activity } from "lucide-react";
import { Diagnosis } from "@/types";

export function ConditionsCard({ conditions }: { conditions: Diagnosis[] }) {
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-base">Active Conditions</CardTitle>
        <Activity className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent className="space-y-3">
        {conditions.length === 0 ? (
          <p className="text-sm text-muted-foreground">No active conditions on record.</p>
        ) : (
          conditions.map((d) => {
            const cfg = diagnosisStatusConfig[d.status];
            return (
              <div key={d.id} className="flex items-center justify-between gap-2">
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium">{d.condition}</p>
                  <p className="text-xs text-muted-foreground">{d.icd10Code}</p>
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
