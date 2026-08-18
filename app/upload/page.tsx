import { AppShell } from "@/components/navigation/app-shell";
import { UploadDropzone } from "@/components/upload/upload-dropzone";
import { UploadsTable } from "@/components/upload/uploads-table";

export default function UploadPage() {
  return (
    <AppShell title="Upload Records">
      <div className="mb-6 max-w-2xl">
        <h2 className="text-2xl font-semibold tracking-tight">Add medical records</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Upload PDFs, scans, or photos and HealthVault AI will extract conditions,
          medications, and results automatically in the background.
        </p>
      </div>

      <div className="max-w-2xl">
        <UploadDropzone />
      </div>

      <div className="mt-10">
        <h3 className="mb-3 text-sm font-semibold">Recent Uploads</h3>
        <UploadsTable />
      </div>
    </AppShell>
  );
}
