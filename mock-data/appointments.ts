import { Appointment } from "@/types";

export const appointments: Appointment[] = [
  {
    id: "apt_001",
    provider: "Dr. Amara Osei",
    specialty: "Endocrinology",
    facility: "Emory Endocrinology",
    date: "2026-09-14T10:30:00",
    status: "scheduled",
    reason: "Quarterly diabetes follow-up",
    location: "1365 Clifton Rd NE, Atlanta, GA",
  },
  {
    id: "apt_002",
    provider: "Dr. Priya Chandran",
    specialty: "Internal Medicine",
    facility: "Emory Primary Care",
    date: "2026-10-02T09:00:00",
    status: "scheduled",
    reason: "Annual physical exam",
    location: "550 Peachtree St NE, Atlanta, GA",
  },
  {
    id: "apt_003",
    provider: "Dr. Sandra Kim",
    specialty: "Ophthalmology",
    facility: "Emory Eye Center",
    date: "2026-11-20T14:00:00",
    status: "scheduled",
    reason: "Annual diabetic eye exam",
    telehealth: false,
  },
  {
    id: "apt_004",
    provider: "Dr. Amara Osei",
    specialty: "Endocrinology",
    facility: "Emory Endocrinology",
    date: "2026-06-10T10:30:00",
    status: "completed",
    reason: "Diabetes & hypertension check-in",
  },
];
