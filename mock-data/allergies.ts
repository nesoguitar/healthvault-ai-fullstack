import { Allergy } from "@/types";

export const allergies: Allergy[] = [
  {
    id: "alg_001",
    allergen: "Penicillin",
    category: "medication",
    reaction: "Hives, facial swelling",
    severity: "severe",
    identifiedDate: "2010-07-01",
    notes: "Confirmed via clinical history; avoid all penicillin-class antibiotics.",
  },
  {
    id: "alg_002",
    allergen: "Tree pollen",
    category: "environmental",
    reaction: "Sneezing, congestion, itchy eyes",
    severity: "mild",
    identifiedDate: "2019-04-22",
  },
  {
    id: "alg_003",
    allergen: "Shellfish",
    category: "food",
    reaction: "Lip swelling, mild hives",
    severity: "moderate",
    identifiedDate: "2015-09-10",
  },
];
