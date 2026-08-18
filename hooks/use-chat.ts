"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { chatApi } from "@/lib/api/resources";

export function useSendChatMessage() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ content, sessionId }: { content: string; sessionId?: string }) =>
      chatApi.sendMessage(content, sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["chat-sessions"] });
    },
  });
}
