"use client";

import { useCallback, useRef, useState } from "react";
import { UploadCloud, CheckCircle2, XCircle, Loader2, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast-provider";
import { useUploadDocument } from "@/hooks/use-documents";
import { ApiError } from "@/lib/api/client";

type UploadState = "uploading" | "success" | "error";

interface StagedFile {
  id: string;
  name: string;
  state: UploadState;
  errorMessage?: string;
}

const ACCEPTED = [".pdf", ".jpg", ".jpeg", ".png"];

export function UploadDropzone() {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState<StagedFile[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();
  const uploadMutation = useUploadDocument();

  const uploadOne = useCallback(
    (file: File) => {
      const id = Math.random().toString(36).slice(2);
      setFiles((prev) => [{ id, name: file.name, state: "uploading" }, ...prev]);

      uploadMutation.mutate(file, {
        onSuccess: () => {
          setFiles((prev) => prev.map((f) => (f.id === id ? { ...f, state: "success" } : f)));
          toast({ title: "Upload complete", description: `${file.name} was accepted and is processing.`, variant: "success" });
        },
        onError: (err) => {
          const message = err instanceof ApiError ? err.message : "Upload failed. Please try again.";
          setFiles((prev) => prev.map((f) => (f.id === id ? { ...f, state: "error", errorMessage: message } : f)));
          toast({ title: "Upload failed", description: message, variant: "error" });
        },
      });
    },
    [uploadMutation, toast]
  );

  const handleFiles = useCallback(
    (fileList: FileList | null) => {
      if (!fileList) return;
      Array.from(fileList).forEach((file) => uploadOne(file));
    },
    [uploadOne]
  );

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    handleFiles(e.dataTransfer.files);
  };

  const removeFile = (id: string) => setFiles((prev) => prev.filter((f) => f.id !== id));

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-14 text-center transition-colors",
          dragActive ? "border-primary bg-primary/5" : "border-border bg-muted/30 hover:bg-muted/50"
        )}
      >
        <span className="flex h-14 w-14 items-center justify-center rounded-full gradient-brand">
          <UploadCloud className="h-6 w-6 text-white" />
        </span>
        <p className="mt-4 text-sm font-semibold">Drag and drop medical records here</p>
        <p className="mt-1 text-xs text-muted-foreground">or click to browse · PDF, JPG, PNG up to 25MB</p>
        <Button className="mt-5" size="sm" onClick={(e) => e.stopPropagation()}>
          Browse files
        </Button>
        <input
          ref={inputRef}
          type="file"
          multiple
          accept={ACCEPTED.join(",")}
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>

      {files.length > 0 && (
        <div className="space-y-3">
          {files.map((f) => (
            <div key={f.id} className="flex items-center gap-3 rounded-xl border border-border bg-card p-4">
              <span
                className={cn(
                  "flex h-10 w-10 shrink-0 items-center justify-center rounded-lg",
                  f.state === "success" && "bg-success/10",
                  f.state === "error" && "bg-destructive/10",
                  f.state === "uploading" && "bg-primary/10"
                )}
              >
                {f.state === "uploading" && <Loader2 className="h-4 w-4 animate-spin text-primary" />}
                {f.state === "success" && <CheckCircle2 className="h-4 w-4 text-success" />}
                {f.state === "error" && <XCircle className="h-4 w-4 text-destructive" />}
              </span>
              <div className="min-w-0 flex-1">
                <div className="flex items-center justify-between gap-2">
                  <p className="truncate text-sm font-medium">{f.name}</p>
                  <button onClick={() => removeFile(f.id)} className="text-muted-foreground hover:text-foreground">
                    <X className="h-4 w-4" />
                  </button>
                </div>
                {f.state === "uploading" && <p className="mt-0.5 text-xs text-muted-foreground">Uploading…</p>}
                {f.state === "success" && <p className="mt-0.5 text-xs text-success">Accepted — processing in the background</p>}
                {f.state === "error" && <p className="mt-1 text-xs text-destructive">{f.errorMessage}</p>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
