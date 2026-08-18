import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { documentStatusConfig } from "@/lib/config";
import { formatDate } from "@/lib/utils";
import { FileStack } from "lucide-react";
import { Document } from "@/types";

export function DocumentsCard({ documents }: { documents: Document[] }) {
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-base">Recent Documents</CardTitle>
        <FileStack className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent className="space-y-3">
        {documents.length === 0 ? (
          <p className="text-sm text-muted-foreground">No documents uploaded yet.</p>
        ) : (
          documents.map((d) => {
            const cfg = documentStatusConfig[d.status];
            return (
              <div key={d.id} className="flex items-center justify-between gap-2">
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium">{d.fileName}</p>
                  <p className="text-xs text-muted-foreground">{formatDate(d.uploadedDate)}</p>
                </div>
                <Badge variant={cfg.badgeVariant}>{cfg.label}</Badge>
              </div>
            );
          })
        )}
        <Link href="/upload">
          <Button variant="ghost" size="sm" className="w-full mt-1">View all documents</Button>
        </Link>
      </CardContent>
    </Card>
  );
}
