"""
Document extraction abstraction, backed by Azure AI Document Intelligence
(prebuilt "layout" / health-related models) when enabled, or a no-op stub
otherwise so the upload pipeline still runs end-to-end in local dev.

Wire-up: the document processing background task (see
app/api/v1/endpoints/documents.py) calls `extract(content, content_type)`
after a file lands in storage, stores the returned text on
Document.extracted_text, and hands it to the embedding step.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.core.config import settings


@dataclass
class ExtractionResult:
    text: str
    summary: str | None = None


class DocumentExtractor(ABC):
    @abstractmethod
    def extract(self, content: bytes, content_type: str) -> ExtractionResult:
        ...


class NoOpExtractor(DocumentExtractor):
    """Used when DOCUMENT_INTELLIGENCE_ENABLED=False. Marks the document as
    processed without OCR, so uploads still complete in local development."""

    def extract(self, content: bytes, content_type: str) -> ExtractionResult:
        return ExtractionResult(
            text="",
            summary="Automatic text extraction is disabled in this environment.",
        )


class AzureDocumentIntelligenceExtractor(DocumentExtractor):
    def __init__(self) -> None:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential

        self._client = DocumentIntelligenceClient(
            endpoint=settings.AZURE_DOCINTEL_ENDPOINT,
            credential=AzureKeyCredential(settings.AZURE_DOCINTEL_API_KEY),
        )

    def extract(self, content: bytes, content_type: str) -> ExtractionResult:
        poller = self._client.begin_analyze_document(
            model_id="prebuilt-layout",
            body=content,
            content_type=content_type,
        )
        result = poller.result()
        text = "\n".join(page_content.content for page_content in (result.paragraphs or []))
        return ExtractionResult(text=text)


def get_document_extractor() -> DocumentExtractor:
    if settings.DOCUMENT_INTELLIGENCE_ENABLED:
        return AzureDocumentIntelligenceExtractor()
    return NoOpExtractor()
