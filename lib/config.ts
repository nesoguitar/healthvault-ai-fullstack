import {
  Stethoscope,
  BedDouble,
  Scissors,
  FlaskConical,
  ScanLine,
  Pill,
  type LucideIcon,
} from "lucide-react";
import { MedicalEventType, LabFlag, DiagnosisStatus, AllergySeverity, DocumentStatus, AppointmentStatus } from "@/types";

export const eventTypeConfig: Record<
  MedicalEventType,
  { label: string; icon: LucideIcon; color: string; bg: string }
> = {
  office_visit: { label: "Office Visit", icon: Stethoscope, color: "text-primary", bg: "bg-primary/10" },
  hospitalization: { label: "Hospitalization", icon: BedDouble, color: "text-destructive", bg: "bg-destructive/10" },
  procedure: { label: "Procedure", icon: Scissors, color: "text-teal", bg: "bg-teal/10" },
  lab_result: { label: "Lab Result", icon: FlaskConical, color: "text-warning", bg: "bg-warning/10" },
  imaging_study: { label: "Imaging Study", icon: ScanLine, color: "text-purple-600", bg: "bg-purple-100" },
  medication_started: { label: "Medication Started", icon: Pill, color: "text-success", bg: "bg-success/10" },
};

export const labFlagConfig: Record<LabFlag, { label: string; badgeVariant: "success" | "warning" | "destructive" }> = {
  normal: { label: "Normal", badgeVariant: "success" },
  high: { label: "High", badgeVariant: "warning" },
  low: { label: "Low", badgeVariant: "warning" },
  critical: { label: "Critical", badgeVariant: "destructive" },
};

export const diagnosisStatusConfig: Record<DiagnosisStatus, { label: string; badgeVariant: "success" | "warning" | "muted" | "default" }> = {
  active: { label: "Active", badgeVariant: "default" },
  chronic: { label: "Chronic", badgeVariant: "warning" },
  resolved: { label: "Resolved", badgeVariant: "muted" },
  in_remission: { label: "In Remission", badgeVariant: "success" },
};

export const allergySeverityConfig: Record<AllergySeverity, { label: string; badgeVariant: "success" | "warning" | "destructive" }> = {
  mild: { label: "Mild", badgeVariant: "success" },
  moderate: { label: "Moderate", badgeVariant: "warning" },
  severe: { label: "Severe", badgeVariant: "destructive" },
  life_threatening: { label: "Life-Threatening", badgeVariant: "destructive" },
};

export const documentStatusConfig: Record<DocumentStatus, { label: string; badgeVariant: "success" | "warning" | "destructive" }> = {
  processed: { label: "Processed", badgeVariant: "success" },
  processing: { label: "Processing", badgeVariant: "warning" },
  failed: { label: "Failed", badgeVariant: "destructive" },
};

export const appointmentStatusConfig: Record<AppointmentStatus, { label: string; badgeVariant: "default" | "success" | "muted" }> = {
  scheduled: { label: "Scheduled", badgeVariant: "default" },
  completed: { label: "Completed", badgeVariant: "success" },
  cancelled: { label: "Cancelled", badgeVariant: "muted" },
};

export const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: "LayoutDashboard" },
  { href: "/upload", label: "Upload Records", icon: "UploadCloud" },
  { href: "/timeline", label: "Health Timeline", icon: "History" },
  { href: "/summary", label: "Patient Summary", icon: "FileText" },
  { href: "/chat", label: "AI Assistant", icon: "MessageSquare" },
  { href: "/settings", label: "Settings", icon: "Settings" },
] as const;
