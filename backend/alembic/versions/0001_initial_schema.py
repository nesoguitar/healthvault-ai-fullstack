"""Initial schema: users, patients, clinical records, documents, chat, audit log

Revision ID: 0001
Revises:
Create Date: 2026-08-15
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

EMBEDDING_DIM = 1536


def upgrade() -> None:
    # pgvector must be enabled before any Vector columns are created.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # --- users ---
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("is_verified", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("mfa_enabled", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("mfa_secret", sa.String(255), nullable=True),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_login_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # --- patients ---
    sex_enum = postgresql.ENUM("male", "female", "other", "unspecified", name="sex_enum")
    sex_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "patients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("date_of_birth", sa.Date, nullable=False),
        sa.Column("sex", sex_enum, nullable=False, server_default="unspecified"),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("blood_type", sa.String(5), nullable=True),
        sa.Column("height_cm", sa.Float, nullable=True),
        sa.Column("weight_kg", sa.Float, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # --- documents (created before medical_events / lab_results, which FK into it) ---
    doc_type_enum = postgresql.ENUM(
        "lab_report", "imaging", "clinical_note", "discharge_summary", "prescription", "other",
        name="document_type_enum",
    )
    doc_type_enum.create(op.get_bind(), checkfirst=True)
    doc_file_type_enum = postgresql.ENUM("pdf", "jpg", "png", name="document_file_type_enum")
    doc_file_type_enum.create(op.get_bind(), checkfirst=True)
    doc_status_enum = postgresql.ENUM("processing", "processed", "failed", name="document_status_enum")
    doc_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("file_name", sa.String(500), nullable=False),
        sa.Column("document_type", doc_type_enum, nullable=False, server_default="other"),
        sa.Column("file_type", doc_file_type_enum, nullable=False),
        sa.Column("size_kb", sa.BigInteger, nullable=False),
        sa.Column("storage_backend", sa.String(20), nullable=False, server_default="local"),
        sa.Column("storage_key", sa.String(1000), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=True),
        sa.Column("status", doc_status_enum, nullable=False, server_default="processing"),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("extracted_text", sa.Text, nullable=True),
        sa.Column("processing_error", sa.Text, nullable=True),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(EMBEDDING_DIM), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_documents_patient_id", "documents", ["patient_id"])
    op.create_index("ix_documents_status", "documents", ["status"])
    # IVFFlat index for approximate nearest-neighbor search over embeddings.
    # Requires rows to exist for good cluster quality; safe to create empty.
    op.execute(
        "CREATE INDEX ix_documents_embedding ON documents "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )

    # --- medical_events ---
    event_type_enum = postgresql.ENUM(
        "office_visit", "hospitalization", "procedure", "lab_result", "imaging_study", "medication_started",
        name="medical_event_type_enum",
    )
    event_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "medical_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_type", event_type_enum, nullable=False),
        sa.Column("event_date", sa.Date, nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("provider", sa.String(255), nullable=True),
        sa.Column("facility", sa.String(255), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("related_document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_medical_events_patient_id", "medical_events", ["patient_id"])
    op.create_index("ix_medical_events_event_type", "medical_events", ["event_type"])
    op.create_index("ix_medical_events_event_date", "medical_events", ["event_date"])

    # --- medications ---
    med_status_enum = postgresql.ENUM("active", "discontinued", "completed", name="medication_status_enum")
    med_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "medications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("generic_name", sa.String(255), nullable=True),
        sa.Column("dosage", sa.String(100), nullable=False),
        sa.Column("frequency", sa.String(100), nullable=False),
        sa.Column("route", sa.String(50), nullable=False),
        sa.Column("prescribed_by", sa.String(255), nullable=False),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("status", med_status_enum, nullable=False, server_default="active"),
        sa.Column("purpose", sa.String(500), nullable=False),
        sa.Column("refills_remaining", sa.Integer, nullable=True),
        sa.Column("instructions", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_medications_patient_id", "medications", ["patient_id"])
    op.create_index("ix_medications_status", "medications", ["status"])

    # --- diagnoses ---
    dx_status_enum = postgresql.ENUM("active", "resolved", "chronic", "in_remission", name="diagnosis_status_enum")
    dx_status_enum.create(op.get_bind(), checkfirst=True)
    dx_severity_enum = postgresql.ENUM("mild", "moderate", "severe", name="diagnosis_severity_enum")
    dx_severity_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "diagnoses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("condition", sa.String(255), nullable=False),
        sa.Column("icd10_code", sa.String(20), nullable=False),
        sa.Column("diagnosed_date", sa.Date, nullable=False),
        sa.Column("status", dx_status_enum, nullable=False),
        sa.Column("severity", dx_severity_enum, nullable=False),
        sa.Column("diagnosed_by", sa.String(255), nullable=False),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_diagnoses_patient_id", "diagnoses", ["patient_id"])
    op.create_index("ix_diagnoses_icd10_code", "diagnoses", ["icd10_code"])
    op.create_index("ix_diagnoses_status", "diagnoses", ["status"])

    # --- allergies ---
    allergy_category_enum = postgresql.ENUM("medication", "food", "environmental", "other", name="allergy_category_enum")
    allergy_category_enum.create(op.get_bind(), checkfirst=True)
    allergy_severity_enum = postgresql.ENUM("mild", "moderate", "severe", "life_threatening", name="allergy_severity_enum")
    allergy_severity_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "allergies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("allergen", sa.String(255), nullable=False),
        sa.Column("category", allergy_category_enum, nullable=False),
        sa.Column("reaction", sa.String(500), nullable=False),
        sa.Column("severity", allergy_severity_enum, nullable=False),
        sa.Column("identified_date", sa.Date, nullable=False),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_allergies_patient_id", "allergies", ["patient_id"])
    op.create_index("ix_allergies_severity", "allergies", ["severity"])

    # --- lab_results ---
    lab_flag_enum = postgresql.ENUM("normal", "high", "low", "critical", name="lab_flag_enum")
    lab_flag_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "lab_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("test_name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("value", sa.Float, nullable=False),
        sa.Column("unit", sa.String(50), nullable=False),
        sa.Column("reference_range", sa.String(100), nullable=False),
        sa.Column("flag", lab_flag_enum, nullable=False),
        sa.Column("result_date", sa.Date, nullable=False),
        sa.Column("ordered_by", sa.String(255), nullable=False),
        sa.Column("source_document_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_lab_results_patient_id", "lab_results", ["patient_id"])
    op.create_index("ix_lab_results_test_name", "lab_results", ["test_name"])
    op.create_index("ix_lab_results_result_date", "lab_results", ["result_date"])
    op.create_index("ix_lab_results_flag", "lab_results", ["flag"])

    # --- appointments ---
    appt_status_enum = postgresql.ENUM("scheduled", "completed", "cancelled", name="appointment_status_enum")
    appt_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", sa.String(255), nullable=False),
        sa.Column("specialty", sa.String(255), nullable=False),
        sa.Column("facility", sa.String(255), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", appt_status_enum, nullable=False, server_default="scheduled"),
        sa.Column("reason", sa.String(500), nullable=False),
        sa.Column("location", sa.String(500), nullable=True),
        sa.Column("telehealth", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"])
    op.create_index("ix_appointments_scheduled_at", "appointments", ["scheduled_at"])
    op.create_index("ix_appointments_status", "appointments", ["status"])

    # --- chat_sessions / chat_messages ---
    chat_role_enum = postgresql.ENUM("user", "assistant", name="chat_role_enum")
    chat_role_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "chat_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_chat_sessions_patient_id", "chat_sessions", ["patient_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", chat_role_enum, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("cited_event_ids", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("cited_document_ids", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(EMBEDDING_DIM), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_chat_messages_session_id", "chat_messages", ["session_id"])
    op.create_index("ix_chat_messages_patient_id", "chat_messages", ["patient_id"])
    op.execute(
        "CREATE INDEX ix_chat_messages_embedding ON chat_messages "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )

    # --- audit_logs ---
    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_ip", sa.String(64), nullable=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(64), nullable=True),
        sa.Column("status_code", sa.Integer, nullable=False),
        sa.Column("detail", sa.String(1000), nullable=True),
    )
    op.create_index("ix_audit_logs_occurred_at", "audit_logs", ["occurred_at"])
    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_resource_id", "audit_logs", ["resource_id"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_index("ix_chat_messages_embedding", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_table("chat_sessions")
    op.execute("DROP TYPE IF EXISTS chat_role_enum")

    op.drop_table("appointments")
    op.execute("DROP TYPE IF EXISTS appointment_status_enum")

    op.drop_table("lab_results")
    op.execute("DROP TYPE IF EXISTS lab_flag_enum")

    op.drop_table("allergies")
    op.execute("DROP TYPE IF EXISTS allergy_severity_enum")
    op.execute("DROP TYPE IF EXISTS allergy_category_enum")

    op.drop_table("diagnoses")
    op.execute("DROP TYPE IF EXISTS diagnosis_severity_enum")
    op.execute("DROP TYPE IF EXISTS diagnosis_status_enum")

    op.drop_table("medications")
    op.execute("DROP TYPE IF EXISTS medication_status_enum")

    op.drop_table("medical_events")
    op.execute("DROP TYPE IF EXISTS medical_event_type_enum")

    op.drop_index("ix_documents_embedding", table_name="documents")
    op.drop_table("documents")
    op.execute("DROP TYPE IF EXISTS document_status_enum")
    op.execute("DROP TYPE IF EXISTS document_file_type_enum")
    op.execute("DROP TYPE IF EXISTS document_type_enum")

    op.drop_table("patients")
    op.execute("DROP TYPE IF EXISTS sex_enum")

    op.drop_table("users")
