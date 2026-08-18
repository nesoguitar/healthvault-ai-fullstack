// ---------------------------------------------
// HealthVault AI — Core Data Models
// ---------------------------------------------

export type Sex = "male" | "female" | "other" | "unspecified";

export interface Patient {
  id: string;
  firstName: string;
  lastName: string;
  dateOfBirth: string; // ISO date
  sex: Sex;
  email: string;
  phone: string;
  avatarUrl?: string;
  bloodType?: string;
  heightCm?: number;
  weightKg?: number;
  address?: string;
  memberSince: string; // ISO date
}

export type MedicalEventType =
  | "office_visit"
  | "hospitalization"
  | "procedure"
  | "lab_result"
  | "imaging_study"
  | "medication_started";

export interface MedicalEvent {
  id: string;
  type: MedicalEventType;
  date: string; // ISO date
  title: string;
  description: string;
  provider?: string;
  facility?: string;
  relatedDocumentId?: string;
  tags?: string[];
}

export type MedicationStatus = "active" | "discontinued" | "completed";

export interface Medication {
  id: string;
  name: string;
  genericName?: string;
  dosage: string;
  frequency: string;
  route: string;
  prescribedBy: string;
  startDate: string;
  endDate?: string;
  status: MedicationStatus;
  purpose: string;
  refillsRemaining?: number;
  instructions?: string;
}

export type DiagnosisStatus = "active" | "resolved" | "chronic" | "in_remission";
export type DiagnosisSeverity = "mild" | "moderate" | "severe";

export interface Diagnosis {
  id: string;
  condition: string;
  icd10Code: string;
  diagnosedDate: string;
  status: DiagnosisStatus;
  severity: DiagnosisSeverity;
  diagnosedBy: string;
  notes?: string;
}

export type LabTrend = "improving" | "worsening" | "stable";
export type LabFlag = "normal" | "high" | "low" | "critical";

export interface LabResult {
  id: string;
  testName: string;
  category: string;
  value: number;
  unit: string;
  referenceRange: string;
  flag: LabFlag;
  date: string;
  orderedBy: string;
  trend?: LabTrend;
  history?: { date: string; value: number }[];
}

export type AllergySeverity = "mild" | "moderate" | "severe" | "life_threatening";

export interface Allergy {
  id: string;
  allergen: string;
  category: "medication" | "food" | "environmental" | "other";
  reaction: string;
  severity: AllergySeverity;
  identifiedDate: string;
  notes?: string;
}

export type DocumentType = "lab_report" | "imaging" | "clinical_note" | "discharge_summary" | "prescription" | "other";
export type DocumentStatus = "processing" | "processed" | "failed";

export interface Document {
  id: string;
  fileName: string;
  type: DocumentType;
  fileType: "pdf" | "jpg" | "png";
  sizeKb: number;
  uploadedDate: string;
  status: DocumentStatus;
  summary?: string;
  url?: string;
}

export type AppointmentStatus = "scheduled" | "completed" | "cancelled";

export interface Appointment {
  id: string;
  provider: string;
  specialty: string;
  facility: string;
  date: string; // ISO datetime
  status: AppointmentStatus;
  reason: string;
  location?: string;
  telehealth?: boolean;
}

export interface Surgery {
  id: string;
  procedure: string;
  date: string;
  surgeon: string;
  facility: string;
  notes?: string;
}

export type ChatRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  createdAt: string;
  citedEventIds?: string[];
}

export interface HealthScoreBreakdown {
  overall: number; // 0-100
  categories: {
    label: string;
    score: number;
    trend: "up" | "down" | "flat";
  }[];
}
