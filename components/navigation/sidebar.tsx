"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  UploadCloud,
  History,
  FileText,
  MessageSquare,
  Settings,
  HeartPulse,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/upload", label: "Upload Records", icon: UploadCloud },
  { href: "/timeline", label: "Health Timeline", icon: History },
  { href: "/summary", label: "Patient Summary", icon: FileText },
  { href: "/chat", label: "AI Assistant", icon: MessageSquare },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar({
  mobileOpen,
  onCloseMobile,
}: {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}) {
  const pathname = usePathname();

  const content = (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between px-5 py-5">
        <Link href="/dashboard" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg gradient-brand">
            <HeartPulse className="h-4.5 w-4.5 text-white" strokeWidth={2.5} />
          </span>
          <span className="text-base font-semibold tracking-tight">HealthVault AI</span>
        </Link>
        {onCloseMobile && (
          <Button variant="ghost" size="icon" className="lg:hidden" onClick={onCloseMobile}>
            <X className="h-5 w-5" />
          </Button>
        )}
      </div>

      <nav className="flex-1 space-y-1 px-3">
        {items.map((item) => {
          const active = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onCloseMobile}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                active
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <Icon className="h-4.5 w-4.5" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="mx-3 mb-4 mt-4 rounded-xl bg-accent p-4">
        <p className="text-xs font-semibold text-accent-foreground">Need help?</p>
        <p className="mt-1 text-xs text-accent-foreground/80">
          Ask your AI assistant anything about your health record.
        </p>
        <Link href="/chat" onClick={onCloseMobile}>
          <Button size="sm" variant="teal" className="mt-3 w-full">
            Open chat
          </Button>
        </Link>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop */}
      <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0 lg:border-r lg:border-border lg:bg-card">
        {content}
      </aside>

      {/* Mobile */}
      {mobileOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="absolute inset-0 bg-black/40" onClick={onCloseMobile} />
          <aside className="absolute inset-y-0 left-0 w-72 bg-card shadow-xl animate-fade-in">
            {content}
          </aside>
        </div>
      )}
    </>
  );
}
