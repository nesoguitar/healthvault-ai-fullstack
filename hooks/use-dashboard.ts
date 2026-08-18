"use client";

import { useQuery } from "@tanstack/react-query";
import { patientsApi } from "@/lib/api/resources";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: patientsApi.dashboard,
  });
}

export function usePatientSummary() {
  return useQuery({
    queryKey: ["patient-summary"],
    queryFn: patientsApi.summary,
  });
}

export function usePatientProfile() {
  return useQuery({
    queryKey: ["patient-profile"],
    queryFn: async () => (await patientsApi.summary()).patient,
  });
}
