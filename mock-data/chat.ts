import { ChatMessage } from "@/types";

export const suggestedPrompts: string[] = [
  "When was my last colonoscopy?",
  "What medications am I taking?",
  "Show my diabetes history.",
  "What were my latest laboratory results?",
];

export const mockChatResponses: Record<string, string> = {
  "when was my last colonoscopy?":
    "I don't see a colonoscopy on record in your uploaded documents or timeline. Your most recent screening procedure was a diabetic eye exam on March 5, 2024. If you've had a colonoscopy elsewhere, you can upload the report and I'll add it to your timeline.",
  "what medications am i taking?":
    "You're currently taking 4 active medications:\n\n• Metformin 1000mg — twice daily, for Type 2 Diabetes\n• Losartan 50mg — once daily, for Hypertension\n• Rosuvastatin 10mg — once daily at bedtime, for Hyperlipidemia\n• Loratadine 10mg — as needed, for seasonal allergies\n\nAll prescriptions are active with refills available except Loratadine, which is taken as needed.",
  "show my diabetes history.":
    "Here's a summary of your Type 2 Diabetes history:\n\n• Diagnosed June 3, 2021 by Dr. Amara Osei, following an A1c of 8.9%\n• Started Metformin 1000mg twice daily on June 5, 2021\n• A1c has steadily improved: 8.9% → 7.8% → 7.2% → 6.9% → 6.7% → 6.6% → 6.5% → 6.4% (most recent, June 2026)\n• Annual diabetic eye exams have shown no signs of retinopathy\n• Kidney function (eGFR, creatinine) has remained stable throughout treatment\n\nYour glycemic control has improved consistently over the past 5 years.",
  "what were my latest laboratory results?":
    "Your most recent labs (June 10, 2026) show:\n\n• Hemoglobin A1c: 6.4% (reference < 5.6%) — trending toward target\n• LDL Cholesterol: 98 mg/dL (reference < 100) — within normal range\n• Total Cholesterol: 172 mg/dL (reference < 200) — normal\n• Creatinine: 1.0 mg/dL (reference 0.7–1.3) — normal\n• eGFR: 92 mL/min/1.73m² (reference > 90) — normal\n• Blood Pressure: 126/82 mmHg — slightly above target\n\nOverall your metabolic panel shows continued improvement, particularly in A1c and LDL trends.",
};

export const initialChatMessages: ChatMessage[] = [
  {
    id: "msg_001",
    role: "assistant",
    content:
      "Hi Nathan, I'm your HealthVault AI assistant. I can help you understand your medical history, medications, and lab results. What would you like to know?",
    createdAt: "2026-08-15T09:00:00",
  },
];
