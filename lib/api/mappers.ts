/**
 * Maps FastAPI (snake_case, backend enum values) responses onto the
 * existing frontend types in types/index.ts (camelCase) — this is what
 * lets every presentational component built for the mock data keep
 * working unmodified against the real API.
 */
import {
  Patient,
  Diagnosis,
  Medication,
  Allergy,
  LabResult,
  MedicalEvent,
  Document,
  Appointment,
  ChatMessage,
  HealthScoreBreakdown,
} from "@/types";

export function mapPatient(p: any): Patient {
  return {
    id: p.id,
    firstName: p.first_name,
    lastName: p.last_name,
    dateOfBirth: p.date_of_birth,
    sex: p.sex,
    email: p.email ?? "",
    phone: p.phone ?? "",
    bloodType: p.blood_type ?? undefined,
    heightCm: p.height_cm ?? undefined,
    weightKg: p.weight_kg ?? undefined,
    address: p.address ?? undefined,
    memberSince: p.created_at ?? p.date_of_birth,
  };
}

export function mapDiagnosis(d: any): Diagnosis {
  return {
    id: d.id,
    condition: d.condition,
    icd10Code: d.icd10_code,
    diagnosedDate: d.diagnosed_date,
    status: d.status,
    severity: d.severity,
    diagnosedBy: d.diagnosed_by,
    notes: d.notes ?? undefined,
  };
}

export function mapMedication(m: any): Medication {
  return {
    id: m.id,
    name: m.name,
    genericName: m.generic_name ?? undefined,
    dosage: m.dosage,
    frequency: m.frequency,
    route: m.route,
    prescribedBy: m.prescribed_by,
    startDate: m.start_date,
    endDate: m.end_date ?? undefined,
    status: m.status,
    purpose: m.purpose,
    refillsRemaining: m.refills_remaining ?? undefined,
    instructions: m.instructions ?? undefined,
  };
}

export function mapAllergy(a: any): Allergy {
  return {
    id: a.id,
    allergen: a.allergen,
    category: a.category,
    reaction: a.reaction,
    severity: a.severity,
    identifiedDate: a.identified_date,
    notes: a.notes ?? undefined,
  };
}

export function mapLabResult(l: any): LabResult {
  return {
    id: l.id,
    testName: l.test_name,
    category: l.category,
    value: l.value,
    unit: l.unit,
    referenceRange: l.reference_range,
    flag: l.flag,
    date: l.result_date,
    orderedBy: l.ordered_by,
  };
}

export function mapMedicalEvent(e: any): MedicalEvent {
  return {
    id: e.id,
    type: e.event_type,
    date: e.event_date,
    title: e.title,
    description: e.description,
    provider: e.provider ?? undefined,
    facility: e.facility ?? undefined,
    relatedDocumentId: e.related_document_id ?? undefined,
    tags: e.tags ?? undefined,
  };
}

export function mapDocument(d: any): Document {
  return {
    id: d.id,
    fileName: d.file_name,
    type: d.document_type,
    fileType: d.file_type,
    sizeKb: d.size_kb,
    uploadedDate: d.uploaded_at,
    status: d.status,
    summary: d.summary ?? undefined,
  };
}

export function mapAppointment(a: any): Appointment {
  return {
    id: a.id,
    provider: a.provider,
    specialty: a.specialty,
    facility: a.facility,
    date: a.scheduled_at,
    status: a.status,
    reason: a.reason,
    location: a.location ?? undefined,
    telehealth: a.telehealth ?? undefined,
  };
}

export function mapChatMessage(m: any): ChatMessage {
  return {
    id: m.id,
    role: m.role,
    content: m.content,
    createdAt: m.created_at,
    citedEventIds: m.cited_event_ids ?? undefined,
  };
}

export function mapHealthScore(h: any): HealthScoreBreakdown {
  return {
    overall: h.overall,
    categories: h.categories.map((c: any) => ({
      label: c.label,
      score: c.score,
      trend: c.trend,
    })),
  };
}
