"use client";

import { Sidebar } from "./sidebar";
import { Navbar } from "./navbar";
import { RequireAuth } from "./require-auth";

export function AppShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <RequireAuth>
      <div className="min-h-screen bg-muted/30">
        <Sidebar />
        <div className="lg:pl-64">
          <Navbar title={title} />
          <main className="px-4 py-6 lg:px-8 lg:py-8">{children}</main>
        </div>
      </div>
    </RequireAuth>
  );
}
