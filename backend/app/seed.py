"""
Seed the database with a realistic demo patient (mirrors the frontend's
mock-data/ fixtures) so the full stack has something to show immediately
after `docker compose up`.

Run with: python -m app.seed
"""
from datetime import date, datetime

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.allergy import Allergy, AllergyCategory, AllergySeverity
from app.models.appointment import Appointment, AppointmentStatus
from app.models.diagnosis import Diagnosis, DiagnosisSeverity, DiagnosisStatus
from app.models.lab_result import LabFlag, LabResult
from app.models.medical_event import MedicalEvent, MedicalEventType
from app.models.medication import Medication, MedicationStatus
from app.models.patient import Patient, Sex
from app.models.user import User

DEMO_EMAIL = "nathan.mekhaeil@example.com"
DEMO_PASSWORD = "DemoPass123!"


def seed() -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == DEMO_EMAIL).first()
        if existing:
            print(f"Demo user {DEMO_EMAIL} already exists — skipping seed.")
            return

        user = User(
            email=DEMO_EMAIL,
            hashed_password=hash_password(DEMO_PASSWORD),
            is_active=True,
            is_verified=True,
        )
        db.add(user)
        db.flush()

        patient = Patient(
            user_id=user.id,
            first_name="Nathan",
            last_name="Mekhaeil",
            date_of_birth=date(1986, 4, 12),
            sex=Sex.male,
            phone="(404) 555-0148",
            address="Atlanta, GA",
            blood_type="O+",
            height_cm=178,
            weight_kg=86,
        )
        db.add(patient)
        db.flush()

        db.add_all(
            [
                Diagnosis(
                    patient_id=patient.id,
                    condition="Type 2 Diabetes Mellitus",
                    icd10_code="E11.9",
                    diagnosed_date=date(2021, 6, 3),
                    status=DiagnosisStatus.chronic,
                    severity=DiagnosisSeverity.moderate,
                    diagnosed_by="Dr. Amara Osei, Endocrinology",
                    notes="Diagnosed following elevated A1c on routine screening.",
                ),
                Diagnosis(
                    patient_id=patient.id,
                    condition="Essential Hypertension",
                    icd10_code="I10",
                    diagnosed_date=date(2020, 11, 18),
                    status=DiagnosisStatus.chronic,
                    severity=DiagnosisSeverity.mild,
                    diagnosed_by="Dr. Priya Chandran, Internal Medicine",
                ),
                Diagnosis(
                    patient_id=patient.id,
                    condition="Hyperlipidemia",
                    icd10_code="E78.5",
                    diagnosed_date=date(2021, 6, 3),
                    status=DiagnosisStatus.chronic,
                    severity=DiagnosisSeverity.mild,
                    diagnosed_by="Dr. Amara Osei, Endocrinology",
                ),
            ]
        )

        db.add_all(
            [
                Medication(
                    patient_id=patient.id,
                    name="Metformin",
                    generic_name="Metformin HCl",
                    dosage="1000 mg",
                    frequency="Twice daily with meals",
                    route="Oral",
                    prescribed_by="Dr. Amara Osei",
                    start_date=date(2021, 6, 5),
                    status=MedicationStatus.active,
                    purpose="Type 2 Diabetes management",
                    refills_remaining=3,
                ),
                Medication(
                    patient_id=patient.id,
                    name="Losartan",
                    generic_name="Losartan Potassium",
                    dosage="50 mg",
                    frequency="Once daily",
                    route="Oral",
                    prescribed_by="Dr. Priya Chandran",
                    start_date=date(2020, 11, 20),
                    status=MedicationStatus.active,
                    purpose="Hypertension management",
                    refills_remaining=5,
                ),
                Medication(
                    patient_id=patient.id,
                    name="Rosuvastatin",
                    generic_name="Rosuvastatin Calcium",
                    dosage="10 mg",
                    frequency="Once daily at bedtime",
                    route="Oral",
                    prescribed_by="Dr. Amara Osei",
                    start_date=date(2021, 6, 10),
                    status=MedicationStatus.active,
                    purpose="Hyperlipidemia / LDL reduction",
                    refills_remaining=2,
                ),
            ]
        )

        db.add(
            Allergy(
                patient_id=patient.id,
                allergen="Penicillin",
                category=AllergyCategory.medication,
                reaction="Hives, facial swelling",
                severity=AllergySeverity.severe,
                identified_date=date(2010, 7, 1),
            )
        )

        a1c_history = [
            (date(2021, 6, 1), 8.9), (date(2021, 12, 1), 7.8), (date(2022, 6, 1), 7.2),
            (date(2023, 1, 15), 6.9), (date(2023, 9, 10), 6.7), (date(2024, 6, 12), 6.6),
            (date(2025, 6, 11), 6.5), (date(2026, 6, 10), 6.4),
        ]
        for d, value in a1c_history:
            db.add(
                LabResult(
                    patient_id=patient.id,
                    test_name="Hemoglobin A1c",
                    category="Metabolic",
                    value=value,
                    unit="%",
                    reference_range="4.0 - 5.6",
                    flag=LabFlag.high,
                    result_date=d,
                    ordered_by="Dr. Amara Osei",
                )
            )

        db.add(
            MedicalEvent(
                patient_id=patient.id,
                event_type=MedicalEventType.office_visit,
                event_date=date(2026, 6, 10),
                title="Diabetes & Hypertension Check-In",
                description="A1c down to 6.4%, closest to target range yet. Blood pressure 126/82.",
                provider="Dr. Amara Osei",
                facility="Emory Endocrinology",
                tags=["diabetes", "hypertension"],
            )
        )

        db.add(
            Appointment(
                patient_id=patient.id,
                provider="Dr. Amara Osei",
                specialty="Endocrinology",
                facility="Emory Endocrinology",
                scheduled_at=datetime(2026, 9, 14, 10, 30),
                status=AppointmentStatus.scheduled,
                reason="Quarterly diabetes follow-up",
                location="1365 Clifton Rd NE, Atlanta, GA",
            )
        )

        db.commit()
        print(f"Seeded demo patient. Login with {DEMO_EMAIL} / {DEMO_PASSWORD}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
