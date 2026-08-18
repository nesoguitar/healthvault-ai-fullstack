import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatDateTime } from "@/lib/utils";
import { CalendarClock } from "lucide-react";
import { Appointment } from "@/types";

export function AppointmentsCard({ appointments }: { appointments: Appointment[] }) {
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-base">Upcoming Appointments</CardTitle>
        <CalendarClock className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent className="space-y-4">
        {appointments.length === 0 ? (
          <p className="text-sm text-muted-foreground">No upcoming appointments scheduled.</p>
        ) : (
          appointments.map((a) => (
            <div key={a.id} className="flex items-start justify-between gap-2">
              <div className="min-w-0">
                <p className="truncate text-sm font-medium">{a.provider}</p>
                <p className="text-xs text-muted-foreground">{a.specialty} · {a.reason}</p>
                <p className="mt-1 text-xs text-muted-foreground">{formatDateTime(a.date)}</p>
              </div>
              <Badge variant="default">Scheduled</Badge>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}
