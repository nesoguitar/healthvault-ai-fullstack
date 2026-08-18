"""
File storage abstraction.

`STORAGE_BACKEND=local` writes to disk under LOCAL_STORAGE_PATH — convenient
for local development, with zero external dependencies.

`STORAGE_BACKEND=azure` writes to Azure Blob Storage. Swapping backends only
requires setting env vars; no route or model code changes. Documents are
stored under a per-patient prefix ("{patient_id}/{uuid}_{filename}") so a
container listing never mixes PHI across patients, and blobs are private
(no public read access) — the API always proxies/signs access.
"""
import hashlib
import os
import uuid
from abc import ABC, abstractmethod
from pathlib import Path

from app.core.config import settings


class StorageBackend(ABC):
    @abstractmethod
    def save(self, *, patient_id: str, file_name: str, content: bytes) -> str:
        """Persist `content` and return a storage_key that can later be used to fetch it."""

    @abstractmethod
    def read(self, storage_key: str) -> bytes:
        """Fetch raw bytes for a previously saved file."""

    @abstractmethod
    def delete(self, storage_key: str) -> None:
        """Remove a file. Prefer soft-deleting the Document row over calling this."""


class LocalStorageBackend(StorageBackend):
    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _resolve(self, storage_key: str) -> Path:
        # Prevent path traversal outside the storage root.
        resolved = (self.base_path / storage_key).resolve()
        if not str(resolved).startswith(str(self.base_path.resolve())):
            raise ValueError("Invalid storage key")
        return resolved

    def save(self, *, patient_id: str, file_name: str, content: bytes) -> str:
        safe_name = f"{uuid.uuid4()}_{Path(file_name).name}"
        storage_key = f"{patient_id}/{safe_name}"
        target = self._resolve(storage_key)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return storage_key

    def read(self, storage_key: str) -> bytes:
        return self._resolve(storage_key).read_bytes()

    def delete(self, storage_key: str) -> None:
        path = self._resolve(storage_key)
        if path.exists():
            os.remove(path)


class AzureBlobStorageBackend(StorageBackend):
    """
    Backed by Azure Blob Storage. Prefer connecting via a managed identity
    (`AZURE_STORAGE_ACCOUNT_URL` + DefaultAzureCredential) in production;
    the connection-string path is provided for simplicity in dev/staging.
    """

    def __init__(self) -> None:
        from azure.storage.blob import BlobServiceClient  # local import: optional dependency

        if settings.AZURE_STORAGE_CONNECTION_STRING:
            self._client = BlobServiceClient.from_connection_string(
                settings.AZURE_STORAGE_CONNECTION_STRING
            )
        elif settings.AZURE_STORAGE_ACCOUNT_URL:
            from azure.identity import DefaultAzureCredential

            self._client = BlobServiceClient(
                account_url=settings.AZURE_STORAGE_ACCOUNT_URL,
                credential=DefaultAzureCredential(),
            )
        else:
            raise RuntimeError(
                "AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_URL must be set "
                "when STORAGE_BACKEND=azure"
            )
        self._container = self._client.get_container_client(settings.AZURE_STORAGE_CONTAINER_NAME)

    def save(self, *, patient_id: str, file_name: str, content: bytes) -> str:
        safe_name = f"{uuid.uuid4()}_{Path(file_name).name}"
        storage_key = f"{patient_id}/{safe_name}"
        self._container.upload_blob(name=storage_key, data=content, overwrite=False)
        return storage_key

    def read(self, storage_key: str) -> bytes:
        return self._container.download_blob(storage_key).readall()

    def delete(self, storage_key: str) -> None:
        self._container.delete_blob(storage_key)


def get_storage_backend() -> StorageBackend:
    if settings.STORAGE_BACKEND == "azure":
        return AzureBlobStorageBackend()
    return LocalStorageBackend(settings.LOCAL_STORAGE_PATH)


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
