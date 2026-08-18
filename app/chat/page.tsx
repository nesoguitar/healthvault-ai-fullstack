"use client";

import { useEffect, useRef, useState } from "react";
import { Send } from "lucide-react";
import { AppShell } from "@/components/navigation/app-shell";
import { ChatBubble } from "@/components/chat/chat-bubble";
import { TypingIndicator } from "@/components/chat/typing-indicator";
import { SuggestedPrompts } from "@/components/chat/suggested-prompts";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ChatMessage } from "@/types";
import { useSendChatMessage } from "@/hooks/use-chat";
import { useToast } from "@/components/ui/toast-provider";
import { ApiError } from "@/lib/api/client";

const WELCOME: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Hi, I'm your HealthVault AI assistant. I can help you understand your medical history, medications, and lab results — grounded in your own record. What would you like to know?",
  createdAt: new Date().toISOString(),
};

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME]);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);
  const sendMutation = useSendChatMessage();
  const { toast } = useToast();

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, sendMutation.isPending]);

  const sendMessage = (content: string) => {
    if (!content.trim()) return;

    const userMsg: ChatMessage = {
      id: Math.random().toString(36).slice(2),
      role: "user",
      content,
      createdAt: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    sendMutation.mutate(
      { content, sessionId },
      {
        onSuccess: (data) => {
          setSessionId(data.sessionId);
          setMessages((prev) => [...prev, data.message]);
        },
        onError: (err) => {
          const message = err instanceof ApiError ? err.message : "Couldn't reach the AI assistant.";
          toast({ title: "Message failed", description: message, variant: "error" });
        },
      }
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  return (
    <AppShell title="AI Health Assistant">
      <div className="flex h-[calc(100vh-8.5rem)] flex-col overflow-hidden rounded-2xl border border-border bg-card">
        <div ref={scrollRef} className="scrollbar-thin flex-1 space-y-5 overflow-y-auto p-5">
          {messages.map((m) => (
            <ChatBubble key={m.id} message={m} />
          ))}
          {sendMutation.isPending && <TypingIndicator />}

          {messages.length <= 1 && !sendMutation.isPending && (
            <div className="pt-2">
              <p className="mb-3 text-xs font-medium text-muted-foreground">Try asking</p>
              <SuggestedPrompts onSelect={sendMessage} />
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="border-t border-border p-4">
          <div className="flex items-end gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage(input);
                }
              }}
              placeholder="Ask about your medications, conditions, or lab results…"
              className="min-h-[44px] flex-1 resize-none"
              rows={1}
            />
            <Button type="submit" size="icon" disabled={!input.trim() || sendMutation.isPending}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <p className="mt-2 text-[11px] text-muted-foreground">
            HealthVault AI can make mistakes. Always confirm important information with your care team.
          </p>
        </form>
      </div>
    </AppShell>
  );
}
