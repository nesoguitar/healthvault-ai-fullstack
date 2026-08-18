import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Pill } from "lucide-react";
import { Medication } from "@/types";

export function MedicationsCard({ medications }: { medications: Medication[] }) {
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-base">Current Medications</CardTitle>
        <Pill className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent className="space-y-3">
        {medications.length === 0 ? (
          <p className="text-sm text-muted-foreground">No active medications on record.</p>
        ) : (
          medications.map((m) => (
            <div key={m.id} className="flex items-center justify-between gap-2">
              <div className="min-w-0">
                <p className="truncate text-sm font-medium">{m.name}</p>
                <p className="text-xs text-muted-foreground">{m.dosage} · {m.frequency}</p>
              </div>
              <Badge variant="teal">Active</Badge>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}
