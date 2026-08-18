import { apiFetch } from "./client";
import {
  mapAllergy,
  mapAppointment,
  mapChatMessage,
  mapDiagnosis,
  mapDocument,
  mapHealthScore,
  mapLabResult,
  mapMedicalEvent,
  mapMedication,
  mapPatient,
} from "./mappers";
import {
  Allergy,
  Appointment,
  ChatMessage,
  Diagnosis,
  Document,
  HealthScoreBreakdown,
  LabResult,
  MedicalEvent,
  Medication,
  Patient,
} from "@/types";

export interface DashboardData {
  patient: Patient;
  healthScore: HealthScoreBreakdown;
  activeConditions: Diagnosis[];
  currentMedications: Medication[];
  recentLabs: LabResult[];
  upcomingAppointments: Appointment[];
  recentDocuments: Document[];
}

export const patientsApi = {
  dashboard: async (): Promise<DashboardData> => {
    const raw = await apiFetch<any>("/patients/me/dashboard");
    return {
      patient: mapPatient(raw.patient),
      healthScore: mapHealthScore(raw.health_score),
      activeConditions: raw.active_conditions.map(mapDiagnosis),
      currentMedications: raw.current_medications.map(mapMedication),
      recentLabs: raw.recent_labs.map(mapLabResult),
      upcomingAppointments: raw.upcoming_appointments.map(mapAppointment),
      recentDocuments: raw.recent_documents.map(mapDocument),
    };
  },

  summary: async () => {
    const raw = await apiFetch<any>("/patients/me/summary");
    return {
      patient: mapPatient(raw.patient),
      diagnoses: raw.diagnoses.map(mapDiagnosis) as Diagnosis[],
      medications: raw.medications.map(mapMedication) as Medication[],
      allergies: raw.allergies.map(mapAllergy) as Allergy[],
      recentLabs: raw.recent_labs.map(mapLabResult) as LabResult[],
    };
  },
};

export const timelineApi = {
  list: async (): Promise<MedicalEvent[]> => {
    const raw = await apiFetch<any[]>("/timeline");
    return raw.map(mapMedicalEvent);
  },
};

export const labsApi = {
  list: async (): Promise<LabResult[]> => {
    const raw = await apiFetch<any[]>("/labs");
    return raw.map(mapLabResult);
  },
  trend: async (testName: string) =>
    apiFetch<{ test_name: string; unit: string; reference_range: string; history: { result_date: string; value: number }[] }>(
      `/labs/trends/${encodeURIComponent(testName)}`
    ),
};

export const documentsApi = {
  list: async (): Promise<Document[]> => {
    const raw = await apiFetch<any[]>("/documents");
    return raw.map(mapDocument);
  },
  upload: async (file: File): Promise<Document> => {
    const form = new FormData();
    form.append("file", file);
    const raw = await apiFetch<any>("/documents", { method: "POST", body: form, isForm: true });
    return mapDocument(raw.document);
  },
};

export const chatApi = {
  sendMessage: async (content: string, sessionId?: string) => {
    const raw = await apiFetch<any>("/chat/messages", {
      method: "POST",
      body: { content, session_id: sessionId },
    });
    return {
      sessionId: raw.session_id as string,
      message: mapChatMessage(raw.message) as ChatMessage,
    };
  },
  listSessions: () => apiFetch<any[]>("/chat/sessions"),
};
