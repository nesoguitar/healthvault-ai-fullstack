"use client";

import { FileText, Image as ImageIcon } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { documentStatusConfig } from "@/lib/config";
import { formatDate } from "@/lib/utils";
import { useDocuments } from "@/hooks/use-documents";
import { AlertCircle, FileStack } from "lucide-react";

const typeLabels: Record<string, string> = {
  lab_report: "Lab Report",
  imaging: "Imaging",
  clinical_note: "Clinical Note",
  discharge_summary: "Discharge Summary",
  prescription: "Prescription",
  other: "Other",
};

export function UploadsTable() {
  const { data: documents, isLoading, isError } = useDocuments();

  if (isLoading) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full rounded-lg" />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-10 text-center">
        <AlertCircle className="h-6 w-6 text-destructive/60" />
        <p className="mt-2 text-sm text-muted-foreground">Couldn't load your documents.</p>
      </div>
    );
  }

  if (!documents || documents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-10 text-center">
        <FileStack className="h-6 w-6 text-muted-foreground/40" />
        <p className="mt-2 text-sm text-muted-foreground">No documents uploaded yet.</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border bg-muted/40 text-left text-xs text-muted-foreground">
              <th className="px-5 py-3 font-medium">File Name</th>
              <th className="px-5 py-3 font-medium">Type</th>
              <th className="px-5 py-3 font-medium">Date Uploaded</th>
              <th className="px-5 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((d) => {
              const cfg = documentStatusConfig[d.status];
              const Icon = d.fileType === "pdf" ? FileText : ImageIcon;
              return (
                <tr key={d.id} className="border-b border-border last:border-0 hover:bg-muted/30">
                  <td className="px-5 py-3">
                    <div className="flex items-center gap-2.5">
                      <Icon className="h-4 w-4 shrink-0 text-muted-foreground" />
                      <span className="max-w-[240px] truncate font-medium sm:max-w-xs">{d.fileName}</span>
                    </div>
                  </td>
                  <td className="px-5 py-3 text-muted-foreground">{typeLabels[d.type]}</td>
                  <td className="px-5 py-3 text-muted-foreground">{formatDate(d.uploadedDate)}</td>
                  <td className="px-5 py-3">
                    <Badge variant={cfg.badgeVariant}>{cfg.label}</Badge>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
