"use client";

import { AppShell } from "@/components/navigation/app-shell";
import { SummarySection } from "@/components/summary/summary-section";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { useToast } from "@/components/ui/toast-provider";
import { usePatientSummary } from "@/hooks/use-dashboard";
import { diagnosisStatusConfig, allergySeverityConfig, labFlagConfig } from "@/lib/config";
import { formatDate } from "@/lib/utils";
import {
  Stethoscope,
  Pill,
  ShieldAlert,
  FlaskConical,
  Download,
  Share2,
  AlertCircle,
} from "lucide-react";

export default function SummaryPage() {
  const { toast } = useToast();
  const { data, isLoading, isError } = usePatientSummary();

  return (
    <AppShell title="Patient Summary">
      {isLoading && (
        <div className="space-y-6">
          <Skeleton className="h-10 w-64" />
          <div className="grid gap-5 lg:grid-cols-2">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={i} className="h-48 rounded-xl" />
            ))}
          </div>
        </div>
      )}

      {isError && (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-16 text-center">
          <AlertCircle className="h-8 w-8 text-destructive/60" />
          <p className="mt-3 text-sm font-medium">Couldn't load your summary</p>
        </div>
      )}

      {data && (
        <>
          <div className="mb-6 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
            <div>
              <h2 className="text-2xl font-semibold tracking-tight">
                {data.patient.firstName} {data.patient.lastName}
              </h2>
              <p className="mt-1 text-sm text-muted-foreground">
                DOB {formatDate(data.patient.dateOfBirth)}
                {data.patient.bloodType ? ` · Blood type ${data.patient.bloodType}` : ""}
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() =>
                  toast({ title: "Summary shared", description: "A secure link was sent to your physician.", variant: "success" })
                }
              >
                <Share2 className="h-4 w-4" />
                Share with physician
              </Button>
              <Button
                onClick={() =>
                  toast({ title: "PDF generated", description: "Your summary has downloaded as a PDF.", variant: "success" })
                }
              >
                <Download className="h-4 w-4" />
                Download PDF
              </Button>
            </div>
          </div>

          <div className="grid gap-5 lg:grid-cols-2">
            <SummarySection title="Conditions" icon={Stethoscope}>
              <div className="space-y-4">
                {data.diagnoses.length === 0 && <p className="text-sm text-muted-foreground">No conditions on record.</p>}
                {data.diagnoses.map((d, i) => {
                  const cfg = diagnosisStatusConfig[d.status];
                  return (
                    <div key={d.id}>
                      {i > 0 && <Separator className="mb-4" />}
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <p className="text-sm font-medium">{d.condition}</p>
                          <p className="text-xs text-muted-foreground">
                            {d.icd10Code} · Diagnosed {formatDate(d.diagnosedDate)} · {d.diagnosedBy}
                          </p>
                          {d.notes && <p className="mt-1.5 text-xs text-muted-foreground/90">{d.notes}</p>}
                        </div>
                        <Badge variant={cfg.badgeVariant}>{cfg.label}</Badge>
                      </div>
                    </div>
                  );
                })}
              </div>
            </SummarySection>

            <SummarySection title="Medications" icon={Pill}>
              <div className="space-y-4">
                {data.medications.length === 0 && <p className="text-sm text-muted-foreground">No medications on record.</p>}
                {data.medications.map((m, i) => (
                  <div key={m.id}>
                    {i > 0 && <Separator className="mb-4" />}
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <p className="text-sm font-medium">{m.name} — {m.dosage}</p>
                        <p className="text-xs text-muted-foreground">{m.frequency} · {m.purpose}</p>
                        <p className="mt-1 text-xs text-muted-foreground/80">Prescribed by {m.prescribedBy}</p>
                      </div>
                      <Badge variant={m.status === "active" ? "teal" : "muted"}>
                        {m.status === "active" ? "Active" : m.status === "discontinued" ? "Discontinued" : "Completed"}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </SummarySection>

            <SummarySection title="Allergies" icon={ShieldAlert}>
              <div className="space-y-4">
                {data.allergies.length === 0 && <p className="text-sm text-muted-foreground">No known allergies.</p>}
                {data.allergies.map((a, i) => {
                  const cfg = allergySeverityConfig[a.severity];
                  return (
                    <div key={a.id}>
                      {i > 0 && <Separator className="mb-4" />}
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <p className="text-sm font-medium">{a.allergen}</p>
                          <p className="text-xs text-muted-foreground">{a.reaction}</p>
                        </div>
                        <Badge variant={cfg.badgeVariant}>{cfg.label}</Badge>
                      </div>
                    </div>
                  );
                })}
              </div>
            </SummarySection>

            <SummarySection title="Recent Labs" icon={FlaskConical}>
              <div className="space-y-4">
                {data.recentLabs.length === 0 && <p className="text-sm text-muted-foreground">No lab results on record.</p>}
                {data.recentLabs.slice(0, 6).map((l) => {
                  const cfg = labFlagConfig[l.flag];
                  return (
                    <div key={l.id} className="flex items-center justify-between gap-2">
                      <div>
                        <p className="text-sm font-medium">{l.testName}</p>
                        <p className="text-xs text-muted-foreground">
                          {l.value} {l.unit} · {formatDate(l.date)} · Ref {l.referenceRange}
                        </p>
                      </div>
                      <Badge variant={cfg.badgeVariant}>{cfg.label}</Badge>
                    </div>
                  );
                })}
              </div>
            </SummarySection>
          </div>
        </>
      )}
    </AppShell>
  );
}
