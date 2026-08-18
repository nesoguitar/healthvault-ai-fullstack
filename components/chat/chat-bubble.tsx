"use client";

import { ChatMessage } from "@/types";
import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { HeartPulse } from "lucide-react";
import { useAuth } from "@/contexts/auth-context";
import { initials } from "@/lib/utils";

export function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const { user } = useAuth();
  const userInitials = user?.email ? initials(user.email.split("@")[0].replace(/[._]/g, " ")) : "You";

  return (
    <div className={cn("flex items-start gap-3", isUser && "flex-row-reverse")}>
      <Avatar className="h-8 w-8 shrink-0 border border-border">
        {isUser ? (
          <AvatarFallback className="text-[11px]">{userInitials}</AvatarFallback>
        ) : (
          <AvatarFallback className="bg-teal/10 text-teal">
            <HeartPulse className="h-3.5 w-3.5" />
          </AvatarFallback>
        )}
      </Avatar>
      <div
        className={cn(
          "max-w-[80%] whitespace-pre-line rounded-2xl px-4 py-2.5 text-sm leading-relaxed sm:max-w-[70%]",
          isUser ? "bg-primary text-primary-foreground rounded-tr-sm" : "bg-card border border-border rounded-tl-sm"
        )}
      >
        {message.content}
      </div>
    </div>
  );
}
