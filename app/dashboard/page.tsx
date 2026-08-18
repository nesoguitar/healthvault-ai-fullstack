"use client";

import { AppShell } from "@/components/navigation/app-shell";
import { HealthScoreCard } from "@/components/dashboard/health-score-card";
import { ConditionsCard } from "@/components/dashboard/conditions-card";
import { MedicationsCard } from "@/components/dashboard/medications-card";
import { LabsCard } from "@/components/dashboard/labs-card";
import { AppointmentsCard } from "@/components/dashboard/appointments-card";
import { DocumentsCard } from "@/components/dashboard/documents-card";
import { Skeleton } from "@/components/ui/skeleton";
import { useDashboard } from "@/hooks/use-dashboard";
import { useAuth } from "@/contexts/auth-context";
import { AlertCircle } from "lucide-react";

function DashboardSkeleton() {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <Skeleton className="h-56 rounded-xl lg:col-span-2" />
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-56 rounded-xl" />
      ))}
    </div>
  );
}

export default function DashboardPage() {
  const { data, isLoading, isError, error } = useDashboard();
  const { user } = useAuth();

  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
  const firstName = data?.patient.firstName || user?.email?.split("@")[0] || "there";

  return (
    <AppShell title="Dashboard">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold tracking-tight">{greeting}, {firstName}</h2>
        <p className="mt-1 text-sm text-muted-foreground">Here's what's happening with your health record.</p>
      </div>

      {isLoading && <DashboardSkeleton />}

      {isError && (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-16 text-center">
          <AlertCircle className="h-8 w-8 text-destructive/60" />
          <p className="mt-3 text-sm font-medium">Couldn't load your dashboard</p>
          <p className="mt-1 max-w-sm text-xs text-muted-foreground">
            {error instanceof Error ? error.message : "Please check that the API is running and try again."}
          </p>
        </div>
      )}

      {data && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <HealthScoreCard healthScore={data.healthScore} />
          <ConditionsCard conditions={data.activeConditions} />
          <MedicationsCard medications={data.currentMedications} />
          <LabsCard labs={data.recentLabs} />
          <AppointmentsCard appointments={data.upcomingAppointments} />
          <DocumentsCard documents={data.recentDocuments} />
        </div>
      )}
    </AppShell>
  );
}
