"use client";

import * as React from "react";
import * as ToastPrimitives from "@radix-ui/react-toast";
import { X, CheckCircle2, AlertCircle, Info } from "lucide-react";
import { cn } from "@/lib/utils";

type ToastVariant = "default" | "success" | "error";

interface ToastItem {
  id: string;
  title: string;
  description?: string;
  variant?: ToastVariant;
}

interface ToastContextValue {
  toast: (t: Omit<ToastItem, "id">) => void;
}

const ToastContext = React.createContext<ToastContextValue | null>(null);

export function useToast() {
  const ctx = React.useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx;
}

const icons: Record<ToastVariant, React.ReactNode> = {
  default: <Info className="h-5 w-5 text-primary" />,
  success: <CheckCircle2 className="h-5 w-5 text-success" />,
  error: <AlertCircle className="h-5 w-5 text-destructive" />,
};

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastItem[]>([]);

  const toast = React.useCallback((t: Omit<ToastItem, "id">) => {
    const id = Math.random().toString(36).slice(2);
    setToasts((prev) => [...prev, { ...t, id }]);
  }, []);

  return (
    <ToastContext.Provider value={{ toast }}>
      <ToastPrimitives.Provider swipeDirection="right">
        {children}
        {toasts.map((t) => (
          <ToastPrimitives.Root
            key={t.id}
            duration={4000}
            onOpenChange={(open) => {
              if (!open) setToasts((prev) => prev.filter((x) => x.id !== t.id));
            }}
            className={cn(
              "flex items-start gap-3 rounded-xl border border-border bg-card p-4 shadow-lg data-[state=open]:animate-fade-in",
              "data-[swipe=end]:translate-x-[var(--radix-toast-swipe-end-x)]"
            )}
          >
            {icons[t.variant || "default"]}
            <div className="flex-1">
              <ToastPrimitives.Title className="text-sm font-semibold">{t.title}</ToastPrimitives.Title>
              {t.description && (
                <ToastPrimitives.Description className="text-sm text-muted-foreground mt-0.5">
                  {t.description}
                </ToastPrimitives.Description>
              )}
            </div>
            <ToastPrimitives.Close className="text-muted-foreground hover:text-foreground">
              <X className="h-4 w-4" />
            </ToastPrimitives.Close>
          </ToastPrimitives.Root>
        ))}
        <ToastPrimitives.Viewport className="fixed bottom-0 right-0 z-[100] flex w-full max-w-sm flex-col gap-2 p-6" />
      </ToastPrimitives.Provider>
    </ToastContext.Provider>
  );
}
